from rest_framework import generics
from .models import Presenca
from aluno.models import Aluno
from oficina.models import Oficina
from .serializers import PresencaSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from aluno.serializers import AlunoSerializer
from rest_framework import status
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from textwrap import wrap
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Frame, Spacer


class PresencaListCreate(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Presenca.objects.all()
    serializer_class = PresencaSerializer

    def create(self, request, *args, **kwargs):
        aluno_id = request.data.get('aluno')
        oficina_id = request.data.get('oficina')

        try:
            presenca = Presenca.objects.get(aluno_id=aluno_id, oficina_id=oficina_id)
            presenca.presente = True
            presenca.save()
            return Response({"message": "Presença atualizada com sucesso."}, status=status.HTTP_200_OK)
        except Presenca.DoesNotExist:
            return super().create(request, *args, **kwargs)


class PresencaListByOficina(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, oficina_id):
        presencas = Presenca.objects.filter(oficina_id=oficina_id, presente=True)
        alunos_presentes = [presenca.aluno for presenca in presencas]
        serializer = AlunoSerializer(alunos_presentes, many=True)
        return Response(serializer.data)

class UnmarkPresence(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, student_id, workshop_id):
        try:
            presence = Presenca.objects.get(aluno_id=student_id, oficina_id=workshop_id)
            presence.presente = False
            presence.save()
            return Response({"message": "Presence successfully unmarked."}, status=status.HTTP_200_OK)
        except Presenca.DoesNotExist:
            return Response({"error": "Presence not found."}, status=status.HTTP_404_NOT_FOUND)

class GenerateCertificate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id, workshop_id):
        try:
            presenca = Presenca.objects.get(aluno_id=student_id, oficina_id=workshop_id, presente=True)
            aluno = presenca.aluno
            oficina = presenca.oficina

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="certificado_{aluno.nome}_{oficina.title}.pdf"'

            p = SimpleDocTemplate(response, pagesize=A4)

            styles = getSampleStyleSheet()
            style = styles["BodyText"]
            style.alignment = TA_JUSTIFY  # Justify text

            text = f"""
            Certificamos que {aluno.nome}, participou da oficina '{oficina.title}' realizada em {oficina.city_of_realization}, no dia {oficina.date_of_realization.strftime('%d/%m/%Y')}, com carga horária de {oficina.workload} horas.
            """

            paragraph = Paragraph(text, style)

            elements = []

            header_text = "ELLP - Ensino Lúdico: Lógica e Programação"
            header_paragraph = Paragraph(f"<b>{header_text}</b>", styles['Title'])
            elements.append(header_paragraph)

            title_text = "Certificado de Participação"
            title_paragraph = Paragraph(f"<b>{title_text}</b>", styles['Heading2'])
            elements.append(title_paragraph)

            elements.append(paragraph)

            signature_text = """
            <br/><br/><br/>
            ______________________________________<br/>
            Assinatura do Responsável<br/>
            ELLP - Ensino Lúdico: Lógica e Programação
            """
            signature_paragraph = Paragraph(signature_text, style)
            elements.append(signature_paragraph)

            p.build(elements)

            return response

        except Presenca.DoesNotExist:
            return HttpResponse("Certificado não disponível. Presença não registrada.", status=404)