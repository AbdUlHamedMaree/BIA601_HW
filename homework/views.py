import json
from wsgiref.simple_server import WSGIRequestHandler
from django.http import JsonResponse
from django.shortcuts import render
from requests import Request
from django.core.handlers.wsgi import WSGIRequest
from json import JSONDecoder

from hw import GeneticAlgorithm, Item


def index(request):
    return render(request, 'homework/index.html')


def run_code(request: WSGIRequest):
    body = JSONDecoder().decode(request.body.decode())

    items = [Item(x['name'], x['benefit'], x['weight']) for x in body['items']]
    elite = body['elite']
    population_size = body['initialPopulationSize']
    mutation_probability = body['mutationProbability']
    max_weight = body['maxWeight']
    iterations = body['times']

    problem = GeneticAlgorithm(max_weight, items, population_size,
                               iterations, mutation_probability, elite)

    return JsonResponse({'message': 'OK', 'logs': problem.solve()})
