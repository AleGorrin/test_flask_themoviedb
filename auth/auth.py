from flask import request, jsonify

# Hardcoded users
USERS = {
    1: {'username': 'admin', 'permission': 'ADMIN'},
    2: {'username': 'consumer', 'permission': 'USER'}
}

def token_required(f):
    def decorator(*args, **kwargs):
        user_id = request.headers.get('Authorization')
        if not user_id:
            return jsonify({'message': 'User ID is missing!'}), 403
        
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({'message': 'Invalid user ID format!'}), 403

        user = USERS.get(user_id)
        if not user:
            return jsonify({'message': 'Invalid user ID!'}), 403
        
        return f(user, *args, **kwargs)
    return decorator

def permission_required(permission):
    def decorator(f):
        def wrapper(user, *args, **kwargs):
            if user['permission'] != permission:
                return jsonify({'message': 'Permission denied!'}), 403
            return f(user, *args, **kwargs)
        return wrapper
    return decorator
