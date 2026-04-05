from django.shortcuts import render
from rest_framework import generics
import subprocess
import os
import tempfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class RunCodeView(APIView):
    permission_classes =[IsAuthenticated]
    
    def post(self, request):
        code = request.data.get('code')
        language = request.data.get('language')
        input_data= request.data.get('input', '')

        try:
            if language=='python':
                with tempfile.NamedTemporaryFile(suffix='.py', mode='w', delete=False) as f:
                    f.write(code)
                    source_file = f.name

                result= subprocess.run(
                    ['python', source_file], 
                    input=input_data,
                    capture_output=True,
                    text = True,
                    timeout=5
                    )   
                os.remove(source_file)

            elif language == "c":
                with tempfile.NamedTemporaryFile(suffix = ".c", mode = "w", delete = False) as f:
                    f.write(code)
                    source_file = f.name
                compiled_file = f.name.replace('.c', '')
                compiled_result = subprocess.run(['gcc', source_file, '-o', compiled_file], capture_output=True, text=True)  
                if compiled_result.returncode!=0:
                    os.remove(source_file)
                    return Response({'output': compiled_result.stderr})
                else:
                    result = subprocess.run(
                        [compiled_file],
                        input=input_data,
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                os.remove(source_file)
                os.remove(compiled_file)

            elif language == "cpp":
                with tempfile.NamedTemporaryFile(suffix = ".cpp", mode = "w", delete = False) as f:
                    f.write(code)
                    source_file = f.name
                compiled_file = f.name.replace('.cpp', '')
                compiled_result = subprocess.run(['g++', source_file, '-o', compiled_file], capture_output=True, text=True)  
                if compiled_result.returncode!=0:
                    os.remove(source_file)
                    return Response({'output':compiled_result.stderr})
                else:
                    result = subprocess.run(
                        [compiled_file],
                        input=input_data,
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                os.remove(source_file)
                os.remove(compiled_file)          


            output = result.stdout if result.returncode==0 else result.stderr 
            return Response({'output':output})

        except subprocess.TimeoutExpired:
            return Response({'output': 'Time Limit Exceeded'})

        except Exception as e:
            return Response({'output': str(e)})   