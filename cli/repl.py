import cmd
from agents.base import Agent

agents = {}

class AgentShell(cmd.Cmd):
    """Command-line interface for managing AI agents.
    
    This class provides a REPL interface for creating, assigning tasks to,
    and managing AI agents in the system.
    """
    intro = "Welcome to hive. Enter help or ? to list the commands"
    prompt = "agent-ants 🐜 > "

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
            print("[!] Use: create researcher 'Role'")
            return
        name, role = args[0], " ".join(args[1:])
        agents[name] = Agent(name, role)
        print(f"[OK] Агент '{name}' created with role '{role}'")

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
            print("[!] Use: assign researcher 'Do something'")
            return
        name = args[0]
        task = " ".join(args[1:])
        agent = agents.get(name)
        if not agent:
            print(f"[ERROR] Agent '{name}' not found")
            return
        response = agent.think(task)
        print(f"\nAgent {name} replied:\n{response}\n")

    def do_exit(self, arg):
        """Exit the agent management interface.
        
        Usage:
            exit
            
        Args:
            arg (str): Not used
            
        Returns:
            bool: True to indicate the end of the command loop
        """
        print("Bye, Kingo")
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
            print(f"[ERROR] Agent '{arg}' not found")
            return
        for idx, m in enumerate(agent.memory):
            print(f"\n[{idx+1}] * {m['task']}\n -> {m['response']}\n")

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
            print(f"🐜 {name}")
