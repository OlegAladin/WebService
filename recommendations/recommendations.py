# recommendations/recommendations.py
from concurrent import futures
import random
import grpc
from recommendations_pb2 import (
 BookCategory,
 BookRecommendation,
 RecommendationResponse,
)
import recommendations_pb2_grpc
books_by_category = {
 BookCategory.MYSTERY: [
 BookRecommendation(id=1, title="Мальтийский сокол"),
 BookRecommendation(id=2, title="Убийство в Восточном экспрессе"),
 BookRecommendation(id=3, title="Собака Баскервилей"),
 BookRecommendation(id=4, title="Автостопом по галактике"),
 BookRecommendation(id=5, title="Игра Эндера"),
 BookRecommendation(id=6, title="Портрет Дориана Грея"),
 BookRecommendation(id=7, title="Призрак дома на холме"),
 BookRecommendation(id=8, title="Чужак"),
 BookRecommendation(id=9, title="Грязная работа"),
 BookRecommendation(id=10, title="Пожирающая серость"),
 ],
 BookCategory.SCIENCE_FICTION: [
 BookRecommendation(id=11, title="Дюна"),
 BookRecommendation(id=12, title="Порог"),
 BookRecommendation(id=13, title="Страсти по Лейбовицу"),
 BookRecommendation(id=14, title="Дитя человеческое"),
 BookRecommendation(id=15, title="Хронолиты"),
 BookRecommendation(id=16, title="КиберЗолушка"),
 BookRecommendation(id=17, title="Заводной апельсин"),
 BookRecommendation(id=18, title="Рассвет"),
 BookRecommendation(id=19, title="Обделённые"),
 BookRecommendation(id=20, title="Идеальное несовершенство"),
 ],
 BookCategory.SELF_HELP: [
 BookRecommendation(id=21, title="Семь навыков высокоэффективных людей"),
 BookRecommendation(id=22, title="Как завоёвывать друзей и оказывать влияние на людей"),
 BookRecommendation(id=23, title="Человек в поисках смысла"),
 BookRecommendation(id=24, title="Токсичные люди"),
 BookRecommendation(id=25, title="Дар психотерапии"),
 BookRecommendation(id=26, title="Не верь всему, что чувствуешь"),
 BookRecommendation(id=27, title="Тревожный мозг"),
 BookRecommendation(id=28, title="Мудрость беспокойства"),
 BookRecommendation(id=29, title="Примируть душу и тело"),
 BookRecommendation(id=30, title="Прочь из замкнутного круга!"),
 ],
}
class RecommendationService(recommendations_pb2_grpc.RecommendationsServicer):

 def Recommend(self, request, context):
  if request.category not in books_by_category:
   context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")
  books_for_category = books_by_category[request.category]
  num_results = min(request.max_results, len(books_for_category))
  books_to_recommend = random.sample(books_for_category, num_results)

  return RecommendationResponse(recommendations=books_to_recommend)
def serve():
 server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
 recommendations_pb2_grpc.add_RecommendationsServicer_to_server(
 RecommendationService(), server
 )
 server.add_insecure_port("[::]:50051")
 server.start()
 server.wait_for_termination()
if __name__ == "__main__":
 serve()