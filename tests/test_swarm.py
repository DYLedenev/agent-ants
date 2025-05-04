from core.swarm import Swarm

def test_swarm_register_and_get():
    swarm = Swarm()
    agent = swarm.register("tester", "debug agent")
    assert agent.name == "tester"

    same_agent = swarm.get("tester")
    assert agent is same_agent

    agent2 = swarm.get("other")
    assert agent2.name == "other"
    assert "other" in swarm.list_agents()
