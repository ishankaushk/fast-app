####qyuery language for reading data in API and its single entry point  ####
import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp


class Query(graphene.ObjectType):
	test = graphene.String(name=graphene.String())
	