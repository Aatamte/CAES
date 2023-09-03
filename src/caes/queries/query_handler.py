from src.caes.artifacts.artifact import Artifact
from src.caes.prompts.prompt import ObservationPrompt


class QueryHandler:
    def __init__(self, environment):
        self.environment = environment
        self.artifacts: dict = {}

        self.query_logs = []

        self.map_query_to_artifact = {}

        self.query_lookup = {}

    def add_artifact(self, artifact: Artifact):
        self.artifacts[artifact.name] = artifact

        # add queries to map_query_to_artifact
        for query in artifact.get_query_space():
            self.map_query_to_artifact[query] = artifact.name
            self.query_lookup[query.__name__] = query

    @staticmethod
    def is_restricted_query(agent, action):
        if type(action) not in agent.action_restrictions:
            return False
        else:
            for restriction in agent.action_restrictions[type(action)]:
                try:
                    restriction(agent, action)
                except AssertionError:
                    return True
        return False

    def process_query(self, agent, query):
        query = self.query_lookup[query["action"]](**query["action_parameters"])
        artifact = self.map_query_to_artifact[type(query)]
        observation = self.artifacts[artifact].process_query(agent, query)

        agent.messages.append(
            {
                "role": "system",
                "content": observation
            }
        )
        return observation


if __name__ == '__main__':
    pass