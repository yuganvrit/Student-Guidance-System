from rest_framework import viewsets, permissions, status  # <-- add status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Question, AssessmentResult
from .serializers import QuestionSerializer, AssessmentResultSerializer
from course.models import Course

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.filter(is_deleted=False)
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

class AssessmentResultViewSet(viewsets.ModelViewSet):
    queryset = AssessmentResult.objects.filter(is_deleted=False)
    serializer_class = AssessmentResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return self.queryset.filter(student=user)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    @action(detail=False, methods=['post'])
    def submit(self, request):
        # ✅ Role check – only students can submit
        if request.user.role != 'student':
            return Response(
                {"detail": "Only students can submit assessments."},
                status=status.HTTP_403_FORBIDDEN
            )

        answers = request.data.get('answers', [])

        if not answers:
            return Response({"error": "No answers provided"}, status=status.HTTP_400_BAD_REQUEST)

        course_scores = {}
        for ans in answers:
            try:
                q = Question.objects.get(id=ans['question_id'])
            except Question.DoesNotExist:
                continue

            if q.correct_option == ans['selected']:
                course_id = q.related_course_id
                if course_id:
                    course_scores[course_id] = course_scores.get(course_id, 0) + 1

        if not course_scores:
            return Response({
                "message": "No correct answers recorded",
                "recommendations": []
            })

        
        top_course_ids = sorted(course_scores, key=course_scores.get, reverse=True)[:2]
        recommended_courses = Course.objects.filter(id__in=top_course_ids, is_deleted=False)

        # save result
        result = AssessmentResult.objects.create(
            student=request.user,
            score=sum(course_scores.values())
        )
        result.course_recommendations.set(recommended_courses)

        return Response(AssessmentResultSerializer(result).data)