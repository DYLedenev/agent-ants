import typer
from core.swarm import Swarm
from core.task import Task

app = typer.Typer()
swarm = Swarm()

@app.command()
def create(name: str, role: str = "assistant"):
    swarm.register(name, role)
    typer.echo(f"[OK] Created agent '{name}' with role: {role}")

@app.command()
def assign(name: str, request: str):
    agent = swarm.get(name)
    task = Task(content=request)
    result = agent.think(task.content)
    typer.echo(f"\nAgent '{name}' says:\n{result}\n")

@app.command(name="list")
def list_agents():
    names = swarm.list_agents()
    if not names:
        typer.echo("[INFO] No agents registered in this session.")
    else:
        typer.echo("🐜 " + "\n🐜 ".join(names))

@app.command()
def exit():
    typer.echo("[INFO] Exiting agentctl.")
    raise typer.Exit()