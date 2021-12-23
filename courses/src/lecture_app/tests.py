from base_app.tests import BaseTestCase


class LectureEndPointTestCase(BaseTestCase):
    def test_create_lecture(self):
        jwt = self.auth('qqq')
        data = {
            'title': 'this is test title lecture',
            'text': 'texllllllllllll',
        }
        course_id = self.create_course()
        resp, resp_data = self.post(f'/api/v1/course/{course_id}/lecture/', data, jwt)

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(data['text'], resp_data['text'])
        self.assertEqual(self.users['qqq']['id'], resp_data['author']['id'])

    def test_get_lecture_not_studying_course(self):
        course_id, lecture_id = self.create_lecture()

        jwt = self.auth('new_student_2')
        resp, resp_data = self.get(f'/api/v1/course/{course_id}/lecture/{lecture_id}/', {}, jwt)
        self.assertEqual(resp.status_code, 404)

        jwt = self.auth('qqq')
        resp, resp_data = self.get(f'/api/v1/course/{course_id}/lecture/{lecture_id}/', {}, jwt)
        self.assertEqual(resp.status_code, 200)

    def test_get_lecture_teaching_course(self):
        course_id, lecture_id = self.create_lecture()

        jwt = self.auth('qqq')
        resp, resp_data = self.get(f'/api/v1/course/{course_id}/lecture/{lecture_id}/', {}, jwt)
        self.assertEqual(resp.status_code, 200)
