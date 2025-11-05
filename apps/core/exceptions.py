from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Chỉ gọi exception handler gốc
    return exception_handler(exc, context)


# def custom_exception_handler(exc, context):
#     """
#     Custom exception handler để format lỗi theo chuẩn chung.
#     """
#     response = exception_handler(exc, context)

#     if response is not None:
#         formatted_response = {
#             "status": response.status_code,
#             "message": response.data.get("detail", "Error"),
#             "errors": response.data,
#         }
#         response.data = formatted_response
#     else:
#         # Trường hợp lỗi không được DRF xử lý (ví dụ: lỗi 500)
#         formatted_response = {"status": 500, "message": str(exc), "errors": {}}
#         response = Response(formatted_response, status=500)

#     return response
