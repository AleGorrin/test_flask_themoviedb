from flask import request, jsonify

# Usuarios con permisos predefinidos
USERS = {
    1: {'username': 'admin', 'permission': 'ADMIN'},
    2: {'username': 'consumer', 'permission': 'USER'}
}

def token_required(f):
    """
    Decorador para verificar que el encabezado 'Authorization' contiene un ID de usuario válido.
    
    Args:
        f (función): La función decorada.
    
    Returns:
        función decorada o mensaje JSON de error si el ID de usuario no es válido.
    """
    def decorator(*args, **kwargs):
        user_id = request.headers.get('Authorization')
        
        # Verificar si el ID de usuario está presente en el encabezado
        if not user_id:
            return jsonify({'message': 'User ID is missing!'}), 403
        
        # Intentar convertir el ID de usuario a entero, devolver error si falla
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({'message': 'Invalid user ID format!'}), 403

        # Verificar si el ID de usuario es válido en la lista de usuarios
        user = USERS.get(user_id)
        if not user:
            return jsonify({'message': 'Invalid user ID!'}), 403
        
        return f(user, *args, **kwargs)
    return decorator

def permission_required(permission):
    """
    Decorador para verificar que el usuario tiene el permiso requerido.
    
    Args:
        permission (str): Permiso necesario para acceder a la función.
    
    Returns:
        función decorada o mensaje JSON de error si el permiso no es suficiente.
    """
    def decorator(f):
        def wrapper(user, *args, **kwargs):
            # Verificar si el permiso del usuario coincide con el requerido
            if user['permission'] != permission:
                return jsonify({'message': 'Permission denied!'}), 403
            return f(user, *args, **kwargs)
        return wrapper
    return decorator
