import logging
import sys
import traceback
from django.shortcuts import render
from django.http import HttpResponseServerError, HttpResponseNotFound, HttpResponseForbidden
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
import uuid

# Configurar logger para errores
logger = logging.getLogger('error_handler')

class ErrorHandlerMiddleware(MiddlewareMixin):
    """
    Middleware personalizado para manejar errores y mostrar páginas amigables al usuario
    """
    
    def process_exception(self, request, exception):
        """
        Maneja excepciones no capturadas y las convierte en respuestas amigables
        """
        # Generar ID único para el error
        error_id = str(uuid.uuid4())[:8].upper()
        
        # Información del contexto para los templates
        context = {
            'error_id': error_id,
            'user': getattr(request, 'user', None),
            'request': request,
        }
        
        # Log del error con detalles técnicos
        self._log_error(request, exception, error_id)
        
        # En modo DEBUG, mostrar el error completo de Django
        if settings.DEBUG:
            return None  # Deja que Django maneje el error normalmente
        
        # Manejar diferentes tipos de errores
        if isinstance(exception, Http404):
            return HttpResponseNotFound(
                render(request, 'errors/404.html', context).content
            )
        elif isinstance(exception, PermissionDenied):
            return HttpResponseForbidden(
                render(request, 'errors/403.html', context).content
            )
        else:
            # Error 500 para cualquier otra excepción
            return HttpResponseServerError(
                render(request, 'errors/500.html', context).content
            )
    
    def _log_error(self, request, exception, error_id):
        """
        Registra el error con todos los detalles técnicos
        """
        try:
            # Información de la excepción
            exc_type, exc_value, exc_traceback = sys.exc_info()
            
            # Detalles de la request
            user_info = "Anonymous"
            if hasattr(request, 'user') and request.user.is_authenticated:
                user_info = f"{request.user.username} (ID: {request.user.id})"
            
            # Información del error
            error_details = {
                'error_id': error_id,
                'exception_type': exc_type.__name__ if exc_type else 'Unknown',
                'exception_message': str(exc_value) if exc_value else 'No message',
                'url': request.get_full_path(),
                'method': request.method,
                'user': user_info,
                'ip_address': self._get_client_ip(request),
                'user_agent': request.META.get('HTTP_USER_AGENT', 'Unknown'),
                'referer': request.META.get('HTTP_REFERER', 'Direct access'),
                'traceback': ''.join(traceback.format_tb(exc_traceback)) if exc_traceback else 'No traceback'
            }
            
            # Log estructurado
            logger.error(
                f"ERROR [{error_id}] {exc_type.__name__}: {exc_value}",
                extra=error_details,
                exc_info=True
            )
            
        except Exception as log_error:
            # Si hay error al logear, al menos intentar un log básico
            logger.error(f"Error logging exception [{error_id}]: {log_error}")
    
    def _get_client_ip(self, request):
        """
        Obtiene la IP real del cliente considerando proxies
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class TemplateErrorHandlerMiddleware(MiddlewareMixin):
    """
    Middleware específico para manejar errores de templates
    """
    
    def process_exception(self, request, exception):
        """
        Maneja errores específicos de templates (TemplateSyntaxError, etc.)
        """
        from django.template import TemplateSyntaxError, TemplateDoesNotExist
        
        if isinstance(exception, (TemplateSyntaxError, TemplateDoesNotExist)):
            error_id = str(uuid.uuid4())[:8].upper()
            
            # Log del error de template
            logger.error(
                f"TEMPLATE ERROR [{error_id}] {type(exception).__name__}: {exception}",
                extra={
                    'error_id': error_id,
                    'url': request.get_full_path(),
                    'template_error': str(exception),
                    'user': getattr(request, 'user', 'Anonymous'),
                }
            )
            
            # En desarrollo, mostrar el error de Django
            if settings.DEBUG:
                return None
            
            # En producción, mostrar página de error amigable
            context = {
                'error_id': error_id,
                'user': getattr(request, 'user', None),
                'request': request,
            }
            
            return HttpResponseServerError(
                render(request, 'errors/500.html', context).content
            )
        
        return None


def handler404(request, exception):
    """
    Vista personalizada para errores 404
    """
    context = {
        'user': getattr(request, 'user', None),
        'request': request,
    }
    return HttpResponseNotFound(
        render(request, 'errors/404.html', context).content
    )


def handler500(request):
    """
    Vista personalizada para errores 500
    """
    error_id = str(uuid.uuid4())[:8].upper()
    
    context = {
        'error_id': error_id,
        'user': getattr(request, 'user', None),
        'request': request,
    }
    
    # Log del error 500
    logger.error(f"500 ERROR [{error_id}] Server error on {request.get_full_path()}")
    
    return HttpResponseServerError(
        render(request, 'errors/500.html', context).content
    )


def handler403(request, exception):
    """
    Vista personalizada para errores 403
    """
    context = {
        'user': getattr(request, 'user', None),
        'request': request,
    }
    return HttpResponseForbidden(
        render(request, 'errors/403.html', context).content
    )