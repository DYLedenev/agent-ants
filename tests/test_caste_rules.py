from agents.base import Agent


def test_minor_cannot_communicate_with_queen():
    queen = Agent(name="queen_test", role="Queen", config={"caste": "queen"})
    minor = Agent(name="minor_test", role="Researcher", config={"caste": "minor"})

    assert not minor.can_communicate_with(queen)


def test_major_can_communicate_with_minor():
    major = Agent(name="major_test", role="Manager", config={"caste": "major"})
    minor = Agent(name="minor_test", role="Researcher", config={"caste": "minor"})

    assert major.can_communicate_with(minor)


def test_queen_can_communicate_with_any():
    queen = Agent(name="queen_test", role="Queen", config={"caste": "queen"})
    for caste in ["major", "minor", "queen"]:
        other = Agent(name=f"agent_{caste}", role="Agent", config={"caste": caste})
        assert queen.can_communicate_with(other)


def test_same_caste_communication():
    a = Agent(name="a", role="Whatever", config={"caste": "major"})
    b = Agent(name="b", role="Whatever", config={"caste": "major"})
    assert a.can_communicate_with(b)


def test_unknown_caste_defaults_to_minor():
    a = Agent(name="a", role="Whatever", config={})
    b = Agent(name="b", role="Whatever", config={"caste": "major"})
    assert not a.can_communicate_with(b)