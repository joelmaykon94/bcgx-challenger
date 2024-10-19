from domain.services.query_service import QueryService


def handle_submit(user_input):
    if user_input:
        return QueryService.get_qna(user_input)
