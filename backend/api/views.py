from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.db.models import Avg, Count
from .models import Dataset, EquipmentData
from .serializers import DatasetSerializer, EquipmentDataSerializer
import pandas as pd
import os

class UploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = DatasetSerializer(data=request.data)
        if file_serializer.is_valid():
            # HISTORY MANAGEMENT: Keep only last 5 (delete older ones BEFORE saving new one to ensure we have space? Or logic: keep 5 total?)
            # Prompt: "Store last 5 uploaded datasets".
            # If we save this one, we have N+1. We want to keep 5 descending.
            # So if we have 5, delete the oldest one (index 4 in descending).
            
            datasets = Dataset.objects.order_by('-uploaded_at')
            if datasets.count() >= 5:
                # We need to delete the oldest ones so that after adding 1 we have 5?
                # Or just keep 5 total.
                # If we have 5, and add 1, we get 6.
                # The prompt says "Store last 5". I'll assume we keep the 5 MOST RECENT.
                # So if count >= 5, delete everything from the 5th onwards (because 0-4 are top 5).
                # But we haven't saved the new one yet. So delete from 4th onwards.
                for d in datasets[4:]:
                   d.delete()

            dataset = file_serializer.save()
            
            # PARSE CSV
            try:
                file_path = dataset.file.path
                # Read CSV
                df = pd.read_csv(file_path)
                # Clean headers
                df.columns = [c.strip() for c in df.columns]

                equipment_list = []
                for _, row in df.iterrows():
                    # Helper to safely get float
                    def get_float(val):
                        try:
                            f = float(val)
                            return 0.0 if pd.isna(f) else f
                        except (ValueError, TypeError):
                            return 0.0

                    eq_name = row.get('Equipment Name') or row.get('equipment_name') or 'Unknown'
                    eq_type = row.get('Type') or row.get('type') or 'Unknown'
                    
                    flow = get_float(row.get('Flowrate') or row.get('flowrate'))
                    press = get_float(row.get('Pressure') or row.get('pressure'))
                    temp = get_float(row.get('Temperature') or row.get('temperature'))
                    
                    equipment_list.append(EquipmentData(
                        dataset=dataset,
                        equipment_name=eq_name,
                        equipment_type=eq_type,
                        flowrate=flow,
                        pressure=press,
                        temperature=temp
                    ))
                
                EquipmentData.objects.bulk_create(equipment_list)
                
                # Double check history limit (if multiple requests came in)
                datasets_check = Dataset.objects.order_by('-uploaded_at')
                if datasets_check.count() > 5:
                    for d in datasets_check[5:]:
                        d.delete()

                return Response(file_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                dataset.delete()
                return Response({'error': f'Error parsing CSV: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HistoryView(APIView):
    def get(self, request):
        datasets = Dataset.objects.order_by('-uploaded_at')[:5]
        serializer = DatasetSerializer(datasets, many=True)
        return Response(serializer.data)

class SummaryView(APIView):
    def get(self, request, dataset_id):
        try:
            dataset = Dataset.objects.get(id=dataset_id)
            data = EquipmentData.objects.filter(dataset=dataset)
            
            if not data.exists():
                 return Response({'error': 'No data found for this dataset'}, status=404)

            total_count = data.count()
            # Averages
            avg_flow = data.aggregate(Avg('flowrate'))['flowrate__avg']
            avg_press = data.aggregate(Avg('pressure'))['pressure__avg']
            avg_temp = data.aggregate(Avg('temperature'))['temperature__avg']
            
            # Type Distribution
            type_dist = list(data.values('equipment_type').annotate(count=Count('equipment_type')))
            
            # Serialize data for table
            table_data = EquipmentDataSerializer(data, many=True).data
            
            return Response({
                'dataset_id': dataset.id,
                'file_name': os.path.basename(dataset.file.name),
                'uploaded_at': dataset.uploaded_at,
                'total_count': total_count,
                'averages': {
                    'flowrate': round(avg_flow, 2) if avg_flow else 0,
                    'pressure': round(avg_press, 2) if avg_press else 0,
                    'temperature': round(avg_temp, 2) if avg_temp else 0
                },
                'type_distribution': type_dist,
                'data': table_data
            })
        except Dataset.DoesNotExist:
            return Response({'error': 'Dataset not found'}, status=404)

from django.http import HttpResponse
from .utils import generate_pdf

class PDFView(APIView):
    def get(self, request, dataset_id):
        try:
            dataset = Dataset.objects.get(id=dataset_id)
            data = EquipmentData.objects.filter(dataset=dataset)
            pdf_buffer = generate_pdf(dataset, data)
            
            response = HttpResponse(pdf_buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="report_{dataset.id}.pdf"'
            return response
        except Dataset.DoesNotExist:
             return Response({'error': 'Dataset not found'}, status=404)
