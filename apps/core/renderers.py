from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    """
    Renderer này tự động chuẩn hóa mọi Response thành dạng thống nhất.
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response", None)
        status_code = getattr(response, "status_code", 200)

        # Nếu dữ liệu có "detail" thì thường là lỗi (ví dụ: 404, 400,...)
        if isinstance(data, dict) and data.get("detail", None):
            formatted = {
                "status": status_code,
                "message": data.get("detail", "Error"),
                "errors": data,
            }
        else:
            formatted = {
                "status": status_code,
                "message": "Success" if status_code < 400 else "Error",
                "data": data,
            }

        return super().render(formatted, accepted_media_type, renderer_context)
