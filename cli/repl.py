import cmd

from agents.base import Agent, Queen
from core.logger import get_logger
from core.task import Task
logger = get_logger("repl")

agents = {}
queen = None

class AgentShell(cmd.Cmd):
    """Command-line interface for managing AI agents.
    
    This class provides a REPL interface for creating, assigning tasks to,
    and managing AI agents in the system.
    """
    intro = "Welcome to hive. Enter help or ? to list the commands"
    prompt = "agent-ants 🐜 > "

    def do_queen(self, arg):
        """Create the Queen agent."""
        global queen
        queen = Queen()
        logger.info("Queen created")

    def do_orchestrate(self, arg):
        """Send a high-level task to the Queen for delegation.

        Usage:
            orchestrate <task description>
        """
        if not queen:
            print("[!] Queen not initialized. Use 'queen' command first.")
            return
        if not agents:
            print("[!] No agents available. Use 'create' to make some agents.")
            return
        task = Task(content=arg)
        results = queen.orchestrate(task, list(agents.values()))
        for t, res in results.items():
            logger.info(f"[+] {t.content}\n -> {res}")
            
    def do_create(self, arg):
        """Create a new agent with a specified name and role.
        
        Usage:
            create <name> <role>
            
        Args:
            arg (str): Command arguments in the format "<name> <role>"
            
        Returns:
            None
            
        Raises:
            ValueError: If incorrect number of arguments are provided
        """
        args = arg.split()
        if len(args) < 2:
            print("[!] Use: create <str: name> <str: role>")
            return
        name, role = args[0], " ".join(args[1:])
        agents[name] = Agent(name, role)
        logger.info(f"Agent '{name}' created with role '{role}'")

    def do_assign(self, arg):
        """Assign a task to a specific agent.
        
        Usage:
            assign <name> <task>
            
        Args:
            arg (str): Command arguments in the format "<name> <task>"
            
        Returns:
            None
            
        Raises:
            ValueError: If incorrect number of arguments are provided
            KeyError: If the specified agent does not exist
        """
        args = arg.split()
        if len(args) < 2:
            print("[!] Use: assign <str: name> <str: do something>")
            return
        name = args[0]
        task = " ".join(args[1:])
        agent = agents.get(name)
        if not agent:
            logger.error(f"Agent '{name}' not found")
            return
        response = agent.think(task)
        logger.info(f"Agent '{name}' replied with:\n{response}")

    def do_exit(self, arg):
        """Exit the agent management interface.
        
        Usage:
            exit
            
        Args:
            arg (str): Not used
            
        Returns:
            bool: True to indicate the end of the command loop
        """
        logger.info("Exiting REPL... Bye, Kingo")
        return True

    def do_log(self, arg):
        """Display the memory (task history) of a specific agent.
        
        Usage:
            log <name>
            
        Args:
            arg (str): The name of the agent whose memory to display
            
        Returns:
            None
            
        Raises:
            KeyError: If the specified agent does not exist
        """
        agent = agents.get(arg)
        if not agent:
            logger.error(f"Agent '{arg}' not found")
            return
        for idx, m in enumerate(agent.memory):
            logger.info(f"[{idx+1}] * {m['task']}\n -> {m['response']}")

    def do_list(self, arg):
        """List all currently active agents.
        
        Usage:
            list
            
        Args:
            arg (str): Not used
            
        Returns:
            None
        """
        for name in agents:
            logger.info(f"🐜 {name}")
            
    def do_list_roles(self, arg):
        """List available task types (roles) from the TaskMapping.

        Usage:
            list_roles

        Args:
            arg (str): Not used

        Returns:
            None
        """
        from core.task import TaskMapping
        mapping = TaskMapping()
        print("Available roles (task types):")
        for role in mapping.get_all_types():
            print(f" - {role}")

    def help_queen(self):
        print("queen\n  Create the Queen agent responsible for orchestrating tasks.")

    def help_orchestrate(self):
        print("orchestrate <task>\n  Let the Queen delegate a complex task to appropriate agents.")
        
    def help_create(self):
        print("create <str: name> [--role <desc>]\n  Create a new agent. Optionally specify a role.")

    def help_assign(self):
        print("assign <str: name> <str: task>\n  Assign a task to an agent and get a response.")

    def help_log(self):
        print("log <str: name>\n  Show all previous tasks/responses for the agent.")

    def help_list(self):
        print("list\n  List all agents registered in the swarm.")

    def help_list_roles(self):
        print("list_roles\n  List all known roles (task types) available in mapping.")

    def help_exit(self):
        print("exit\n  Exit the agent REPL.")
        
    def do_help(self, arg):
        if arg:
            return super().do_help(arg)
        print("\nAvailable commands:\n")
        print("  queen                               Create the Queen agent")
        print("  orchestrate <task>                  Delegate task via the Queen")
        print("  create <str: name> [--role <desc>]     Create a new agent with optional role")
        print("  assign <str: name> <task>              Assign a task to the agent")
        print("  log <str: name>                        Show agent's memory log")
        print("  list                              List all available agents in the swarm")
        print("  list_roles                        Show all available roles from mapping")
        print("  exit                              Exit the application")
        print("\nType 'help <command>' for more info.")
