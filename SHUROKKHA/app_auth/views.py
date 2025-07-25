from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import AppUserSerializer
from rest_framework.authtoken.models import Token
from .models import AppUser,AppUserToken
from django.contrib.auth.hashers import check_password



@api_view(['POST'])
def register_user(request):
    print("=== RECEIVED DATA ===", request.data)
    print("=== RECEIVED FILES ===", request.FILES)

    # Flatten the fields (MultiValueDict -> regular dict, because ekta data field not multiple)
    flat_data = {key: request.data.get(key) for key in request.data}
    flat_files = {key: request.FILES.get(key) for key in request.FILES}

    print("=== FLATTENED DATA ===", flat_data)
    print("=== FLATTENED FILES ===", flat_files)

    serializer = AppUserSerializer(data={**flat_data, **flat_files})

    if serializer.is_valid():
        serializer.save()
        print("User saved successfully.")
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

    print("Validation Errors:", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = AppUser.objects.get(username=username)
    except AppUser.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    if not check_password(password, user.password):
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    #Get or create token
    token, _ = AppUserToken.objects.get_or_create(user=user)

    return Response({
        'message': 'Login successful',
        'token': token.key,
        'user': {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'date_of_birth': user.date_of_birth,
            'nid_number': user.nid_number,
            'Father_name': user.Father_name,
            'Mother_name': user.Mother_name,
            'address': user.address,
            'phone_number': user.phone_number,
            'selfie_image': user.selfie_image.url if user.selfie_image else None,
        }
    }, status=status.HTTP_200_OK)