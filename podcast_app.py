# podcast_app.py
import asyncio
import sys
from workflow import workflow
from agent_framework import AgentExecutorRequest, AgentRunUpdateEvent, WorkflowOutputEvent, ChatMessage, Role

# ANSI color codes
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def show_loading(message="Processing"):
    """Show a loading indicator."""
    sys.stdout.write(f"{Colors.YELLOW}{message}... {Colors.RESET}")
    sys.stdout.flush()


def clear_loading():
    """Clear the loading indicator."""
    sys.stdout.write("\r" + " " * 80 + "\r")
    sys.stdout.flush()

class PodcastGenerator:
    """Podcast生成器"""
    
    def __init__(self):
        self.workflow = workflow
    
    async def generate_podcast(self):
        """生成podcast"""
        print("🎙️ Starting Podcast Generator...")
        print("=" * 50)
        
        try:
            # 启动workflow
            start_request = AgentExecutorRequest(
                messages=[
                    ChatMessage(
                        role=Role.USER,
                        text="Generate a podcast script"
                    )
                ],
                should_respond=True
            )
            
            # 运行workflow
            result = await self.workflow.run(start_request)
            
            # 提取podcast脚本
            podcast_script = self._extract_podcast_script(result)
            
            # 保存到文件
            self._save_to_file(podcast_script)
            
            print("\n" + "=" * 50)
            print("✅ Podcast generated and saved to podcast.txt!")
            print("=" * 50)
            
            return podcast_script
            
        except Exception as e:
            print(f"❌ Error generating podcast: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _extract_podcast_script(self, result):
        """从结果中提取podcast脚本"""
        pending_responses = None
        loading_shown = False

        # Process events
        for event in result:
            # Agent response updates
            if isinstance(event, AgentRunUpdateEvent):
                # Get agent name from executor_id
                agent_name = event.executor_id

                # Print agent name header when agent changes
                if agent_name != current_agent:
                    # Clear loading indicator if shown
                    if loading_shown:
                        clear_loading()
                        loading_shown = False

                    current_agent = agent_name
                    print(f"\n{Colors.BOLD}[{agent_name.upper()}]:{Colors.RESET}")

                    # Show loading before first output
                    if not event.data or not event.data.text:
                        show_loading(f"Waiting for {agent_name}")
                        loading_shown = True

                # Print agent response text in green
                if event.data and event.data.text:
                    # Clear loading if shown
                    if loading_shown:
                        clear_loading()
                        loading_shown = False

                    print(f"{Colors.GREEN}{event.data.text}{Colors.RESET}", end="", flush=True)

            # Workflow output (final)
            elif isinstance(event, WorkflowOutputEvent):
                # Clear loading if shown
                if loading_shown:
                    clear_loading()
                    loading_shown = False

                print("\n")
                print("=" * 60)
                print(f"{Colors.BOLD}{Colors.GREEN}WORKFLOW COMPLETE{Colors.RESET}")
                print("=" * 60)
                print(f"\n{Colors.GREEN}{event.data}{Colors.RESET}")
                return event.data

        
        # 默认脚本
        return """[INTRO MUSIC]

HOST: Welcome to the Daily Podcast! Today we're discussing interesting topics.

This is a sample podcast script generated automatically.

[OUTRO MUSIC]

Thank you for listening!"""
    
    def _save_to_file(self, script):
        """保存脚本到文件"""
        with open('podcast.txt', 'w', encoding='utf-8') as f:
            f.write(script)


def main():
    """Run the podcast workflow application."""
    print("=" * 60)
    print("Welcome to Podcast Application")
    print("=" * 60)
    print()
    
    # 创建生成器
    generator = PodcastGenerator()
    
    try:
        # 运行异步任务
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        podcast = loop.run_until_complete(generator.generate_podcast())
        
        # 显示部分内容预览
        if podcast:
            print("\n📝 Preview of podcast.txt:")
            print("-" * 40)
            lines = podcast.split('\n')
            for i, line in enumerate(lines[:15]):  # 显示前15行
                if line.strip():
                    print(line)
            if len(lines) > 15:
                print("... (see podcast.txt for full script)")
            print("-" * 40)
        
        loop.close()
        
    except KeyboardInterrupt:
        print("\n⏹️ Generation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
   main()