from flask_restful import Resource
from http import HTTPStatus
from flask import request

from instruction import instructions_list, Instruction


class InstructionListRecourse(Resource):
    def get(self):
        data = []

        for instruction in instructions_list:
            if instruction.is_publish:
                data.append(instruction.data)

        return {'data': data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()

        instruction = Instruction(data['name'], data['description'], data['steps'], data['tools'], data['cost'],
                                  data['duration'])

        instructions_list.append(instruction)

        return instruction.data, HTTPStatus.CREATED


class InstructionResource(Resource):
    def get(self, instruction_id):
        instruction = next((instruction for instruction in instructions_list if instruction.id ==
                            instruction_id and instruction.is_publish), None)

        if instruction is None:
            return {'message': 'instruction not found'}, HTTPStatus.NOT_FOUND

        return instruction.data, HTTPStatus.OK

    def put(self, instruction_id):
        data = request.get_json()

        instruction = next((instruction for instruction in instructions_list if instruction.id ==
                            instruction_id and instruction.is_publish), None)

        if instruction is None:
            return {'message': 'instruction not found'}, HTTPStatus.NOT_FOUND

        instruction.name = data['name']
        instruction.description = data['description']
        instruction.steps = data['steps']
        instruction.tools = data['tools']
        instruction.cost = data['cost']
        instruction.duration = data['duration']

        return instruction.data, HTTPStatus.OK


class InstructionPublic(Resource):
    def put(self, instruction_id):
        instruction = next((instruction for instruction in instructions_list if instruction.id ==
                            instruction_id), None)

        if instruction is None:
            return {'message': 'instruction not found'}, HTTPStatus.NOT_FOUND

        instruction.is_publish = True

        return {}, HTTPStatus.NO_CONTENT

    def delete(self, instruction_id):
        instruction = next((instruction for instruction in instructions_list if instruction.id ==
                            instruction_id), None)

        if instruction is None:
            return {'message': 'instruction not found'}, HTTPStatus.NOT_FOUND

        instruction.is_publish = False

        return {}, HTTPStatus.NO_CONTENT
