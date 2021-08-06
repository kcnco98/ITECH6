import os
import re
import inspect
import tempfile
import rango.models
from rango import forms
from populate_rango import populate
from django.db import models
from django.test import TestCase
from django.conf import settings
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.forms import fields as django_fields

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

f"{FAILURE_HEADER} {FAILURE_FOOTER}"


def create_user_object():
    """
    Helper function to create a User object.
    """
    user = User.objects.get_or_create(username='testuser',
                                      first_name='Test',
                                      last_name='User',
                                      email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()

    return user


def get_template(path_to_template):
    """
    Helper function to return the string representation of a template file.
    """
    f = open(path_to_template, 'r')
    template_str = ""

    for line in f:
        template_str = f"{template_str}{line}"

    f.close()
    return template_str


class LearningListTests(TestCase):

    def test_learninglist_class(self):

        self.assertTrue('LearningList' in dir(rango.models))
        learning_list = rango.models.LearningList()

        expected_attributes = {
            'user': create_user_object(),
        }

        expected_types = {
            'user': models.fields.related.OneToOneField,
        }

        found_count = 0

        for attr in learning_list._meta.fields:
            attr_name = attr.name

            for expected_attr_name in expected_attributes.keys():
                if expected_attr_name == attr_name:
                    found_count += 1

                    self.assertEqual(type(attr), expected_types[attr_name],
                                     f"{FAILURE_HEADER}The type of attribute for '{attr_name}' was '{type(attr)}'; we expected '{expected_types[attr_name]}'. Check your definition of the UserProfile model.{FAILURE_FOOTER}")
                    setattr(learning_list, attr_name, expected_attributes[attr_name])

        self.assertEqual(found_count, len(expected_attributes.keys()),
                         f"{FAILURE_HEADER}In the LearningList model, we found {found_count} attributes, but were expecting {len(expected_attributes.keys())}. Check your implementation and try again.{FAILURE_FOOTER}")
        learning_list.save()


class LearningListTests(TestCase):

    def test_new_learninglist_view_exists(self):
        url = ''

        try:
            url = reverse('rango:learning_list')
        except:
            pass

        self.assertEqual(url, '/rango/learning_list/',
                         f"{FAILURE_HEADER}Have you created the rango:learning_list URL mapping correctly? It should point "
                         f"to the new show_learning_list() view, and have a URL of '/rango/learning_list/' Remember "
                         f"the first part of the URL (/rango/) is handled by the project's urls.py module, "
                         f"and the second part (learning_list/) is handled by the Rango app's urls.py module."
                         f"{FAILURE_FOOTER}")

    def test_learninglist_template(self):
        """
        Does the learning_list.html template exist in the correct place, and does it make use of template inheritance?
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'rango')
        template_path = os.path.join(template_base_path, 'learning_list.html')
        self.assertTrue(os.path.exists(template_path),
                        f"{FAILURE_HEADER}We couldn't find the 'learning_list.html' template in the 'templates/rango/' "
                        f"directory. Did you put it in the right place?{FAILURE_FOOTER}")

        template_str = get_template(template_path)

        full_head_pattern = r'<h1>(\s*|\n*)Here are some links you are interested in(\s*|\n*)</h1>'
        block_title_pattern = r'{% block title_block %}(\s*|\n*)Learning List(\s*|\n*){% (endblock|endblock title_block) %}'
        request = self.client.get(reverse('rango:learning_list'))
        content = request.content.decode('utf-8')

        self.assertTrue(re.search(full_head_pattern, content),
                        f"{FAILURE_HEADER}The <title> of the response for 'rango:learning_list' is not correct. Check your "
                        f"learning_list.html template, and try again.{FAILURE_FOOTER}")
        self.assertTrue(re.search(block_title_pattern, template_str),
                        f"{FAILURE_HEADER}Is learning_list.html using template inheritance? Is your <title> block correct?{FAILURE_FOOTER}")

    def test_learninglist_get_response(self):

        request = self.client.get(reverse('rango:learning_list'))
        content = request.content.decode('utf-8')

        self.assertTrue('<h1>Here are some links you are interested in</h1>' in content,
                        f"{FAILURE_HEADER}We couldn't find the '<h1>Here are some links you are interested in</h1>' "
                        f"header tag in your learninglist template. Did you follow the specification in the book to the "
                        f"letter?{FAILURE_FOOTER}")
