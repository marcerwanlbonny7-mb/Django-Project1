from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(destinataire=self.request.user)


class NotificationLireView(APIView):
    def patch(self, request, pk):
        notification = Notification.objects.filter(pk=pk, destinataire=request.user).first()
        if not notification:
            return Response({'detail': 'Notification non trouvée.'}, status=status.HTTP_404_NOT_FOUND)
        notification.lu = True
        notification.save()
        return Response({'detail': 'Notification marquée comme lue.'})


class NotificationLireToutView(APIView):
    def patch(self, request):
        Notification.objects.filter(destinataire=request.user, lu=False).update(lu=True)
        return Response({'detail': 'Toutes les notifications ont été marquées comme lues.'})
