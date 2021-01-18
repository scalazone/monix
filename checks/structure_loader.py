from structure import *
import json
from pathlib import Path
from envs import CONTENT_PATH


def load_structure():
  courses = [load_course('monix')]
  levels = load_levels(courses)
  topics = load_topics(courses)
  return Structure(courses, levels, topics)


def load_course(course_id: str):
  try:
    path = f'{CONTENT_PATH}/index.json'
    course_json = Path(path).read_text()
    course = json.loads(course_json)
    return Course(course_id, course['name'], course['levels'], course['image'],
                  course['video'], course['desc'], course['language'], course['scope'])
  except FileNotFoundError:
    assert False, f'Index file not found for course {course_id}'
  except KeyError as e:
    assert False, f'Course {course_id} index is malformed, cause: {repr(e)}'


def load_levels(courses: [Course]):
  return [load_level(course.id, level) for course in courses for level in course.levels]


def load_level(course_id: str, level_id: str):
  try:
    path = f'{CONTENT_PATH}/{level_id}.json'
    level_json = Path(path).read_text()
    level = json.loads(level_json)
    ranges = [TopicRange(range['topicId'], range['lessonStart'], range['lessonEnd']) for range in level['ranges']]
    return Level(level_id, course_id, level['name'], level['desc'], ranges)
  except FileNotFoundError:
    assert False, f'Level {level} file not found for course {course_id}'
  except KeyError as e:
    assert False, f'Level {level} file for course {course_id} is malformed, cause: {repr(e)}'

def load_topics(courses: [Course]):
  return dict([load_topics_for_course(course.id) for course in courses])


def load_topics_for_course(course_id: str):
  try:
    topics_index_json = Path(f'{CONTENT_PATH}/topics/index.json').read_text()
    topics_index = json.loads(topics_index_json)
    return (course_id, [load_topic(course_id, topic_id) for topic_id in topics_index['topics']])
  except FileNotFoundError:
    assert False, f'Topics index file not found'
  except KeyError as e:
    assert False, f'Topics index is malformed, cause: {repr(e)}'


def empty_if_none(array):
  return [] if array == None else array


def load_topic(course_id: str, topic_id: str):
  try:
    path = f'{CONTENT_PATH}/topics/{topic_id}/index.json'
    topic_json = Path(path).read_text()
    topic = json.loads(topic_json)
    lessons = [Lesson(lesson['id'], topic_id, lesson['title'], lesson['authorIds'], lesson['duration'],
                      [LessonPrereq(prereq['lessonId'], prereq['topicId']) for prereq in
                       empty_if_none(lesson.get('prerequisites'))])
               for lesson in topic['lessons']]
    return Topic(topic_id, topic['name'], topic['desc'], lessons)
  except FileNotFoundError:
    assert False, f'Topic {topic_id} index not found'
  except KeyError as e:
    assert False, f'Topic {topic_id} index is malformed, cause: {repr(e)}'
