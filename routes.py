from flask import Flask, redirect, render_template, request, url_for
from server import app, question_list, survey_name, n
import csv
from surveys import surveys
from questions import questions