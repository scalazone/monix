from dataclasses import dataclass


@dataclass
class Course:
  id: str
  name: str
  course_level_types: [str]
  image: str
  video: str
  description: str
  language: str
  scope: [str]


@dataclass
class TopicRange:
  topic_id: str
  lesson_start: str
  lesson_end: str

@dataclass
class Level:
  level: str
  course_id: str
  name: str
  description: str
  ranges: [TopicRange]


@dataclass
class Lesson:
  id: str
  topic_id: str
  title: str
  author_ids: [str]
  duration: int
  prereqs: [str]


@dataclass
class LessonPrereq:
  lesson_id: str
  topic_id: str

@dataclass
class Topic:
  id: str
  name: str
  description: str
  lessons: [Lesson]


@dataclass
class Structure:
  courses: [Course]
  levels: [Level]
  topics: dict
