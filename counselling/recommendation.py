# recommendation/services/recommendation_engine.py
from assessment.models import StudentSkillResult
from career.models import CareerSkill, Career, CareerPath


class CareerRecommendationEngine:
    """
    Matches student skills to career requirements.
    Uses minimum_score (0-100) and weightage for ranking.
    """

    def __init__(self, student):
        self.student = student
        self.student_skills = self._get_student_skills()

    def _get_student_skills(self):
        """Get latest skill scores from completed assessments."""
        results = StudentSkillResult.objects.filter(
            student_assessment__student=self.student,
            student_assessment__status='completed'
        ).select_related('skill')

        return {result.skill_id: result.score for result in results}

    def calculate_match(self, career):
        """
        Returns: (match_score 0-100, gap_skills list, is_ready bool)
        """
        required = career.career_skills.filter(
            is_deleted=False
        ).select_related('skill')

        if not required.exists():
            return 0, [], False

        total_weighted = 0
        total_weight = 0
        gap_skills = []

        for req in required:
            student_score = self.student_skills.get(req.skill_id, 0)

            # Match ratio (capped at 1.0 = 100%)
            match = min(student_score / req.minimum_score, 1.0) if req.minimum_score > 0 else 1.0
            total_weighted += match * req.weightage
            total_weight += req.weightage

            # Track gaps
            if student_score < req.minimum_score:
                gap_skills.append({
                    'skill_id': req.skill_id,
                    'skill_name': req.skill.name,
                    'required_score': req.minimum_score,
                    'student_score': student_score,
                    'gap': req.minimum_score - student_score,
                    'weightage': req.weightage
                })

        match_score = round((total_weighted / total_weight) * 100) if total_weight > 0 else 0
        is_ready = len(gap_skills) == 0

        return match_score, gap_skills, is_ready

    def get_recommendations(self, min_match=30, top_n=5):
        careers = Career.objects.filter(is_deleted=False)
        results = []

        for career in careers:
            match_score, gaps, is_ready = self.calculate_match(career)

            if match_score >= min_match:
                results.append({
                    'career_id': career.id,
                    'career_title': career.title,
                    'industry': career.industry,
                    'match_score': match_score,
                    'is_ready': is_ready,
                    'total_skills': career.career_skills.filter(is_deleted=False).count(),
                    'met_skills': career.career_skills.filter(is_deleted=False).count() - len(gaps),
                    'gap_skills': sorted(gaps, key=lambda x: -x['weightage'])[:3],
                    # Pull learning path if career is recommended
                    'learning_path': self._get_learning_path(career) if match_score >= 60 else []
                })

        results.sort(key=lambda x: -x['match_score'])
        return results[:top_n]

    def _get_learning_path(self, career):
        """Fetch the pre-defined course sequence for this career."""
        paths = CareerPath.objects.filter(
            career=career,
            is_deleted=False
        ).select_related('course').order_by('sequence_number')

        return [
            {
                'sequence': p.sequence_number,
                'course_id': p.course.id,
                'course_title': p.course.title,
            }
            for p in paths
        ]