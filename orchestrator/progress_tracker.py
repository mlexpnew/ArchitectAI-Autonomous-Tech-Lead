from orchestrator.project_state import ProjectState


class ProgressTracker:

    def __init__(self):

        self.state = None

    def start(self, project):

        self.state = ProjectState(project)

    def running(self, agent):

        self.state.current = agent

        self.state.status = "Running"

        print(f"[RUNNING] {agent}")

    def completed(self, agent):

        self.state.completed.append(agent)

        self.state.current = ""

        print(f"[DONE] {agent}")

    def failed(self, agent):

        self.state.failed.append(agent)

        self.state.current = ""

        print(f"[FAILED] {agent}")

    def summary(self):

        print("\n========== PROJECT ==========")

        print("Project :", self.state.project_name)

        print("Completed :", self.state.completed)

        print("Failed :", self.state.failed)

        print("=============================\n")