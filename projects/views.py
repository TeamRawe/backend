from users.role_restrictons import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@role_required(['ADMIN'])
@assignment_required(['ACTIVE', 'FREEZED'])
def test_assign(request, project_id, stage_id):
    user = request.user
    return Response({"message": f"Hello, {user.first_name}! You are allowed on this target"})
