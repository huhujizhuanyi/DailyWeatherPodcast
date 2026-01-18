from datetime import datetime
from dataclasses import dataclass

from agent_framework import (
    WorkflowBuilder,
    WorkflowContext,
    Executor,
    AgentExecutorResponse,
    AgentExecutorRequest,
    ChatMessage,
    Role,
    handler,
    AgentExecutor,
)
from search_agent import setup_search_agent
from generate_script_agent import setup_gen_script_agent


@dataclass
class ScriptApprovalRequest:
    """Request for user to approve or reject the generated script."""
    prompt: str
    generated_script: str

class SimpleWeatherWorkflow(Executor):
    """最简单的天气workflow"""

    def __init__(self, id: str):
        super().__init__(id=id)
        self.step = "get_weather"

    @handler
    async def start(self, request: AgentExecutorRequest, ctx: WorkflowContext) -> None:
        """开始工作流"""
        # 直接搜索天气
        today = datetime.now()
        await ctx.send_message(
            AgentExecutorRequest(
                messages=[ChatMessage(
                    role=Role.USER,
                    text="What's the weather like today in Shanghai? Today is {}. Besides, please give me some tips".format(today.date())
                )],
                should_respond=True
            ),
            target_id="search_executor"
        )

    @handler
    async def handle_response(self, response: AgentExecutorResponse, ctx: WorkflowContext) -> None:
        """处理响应"""
        # 提取响应文本
        text = ""
        if hasattr(response, 'agent_run_response') and hasattr(response.agent_run_response, 'text'):
            text = response.agent_run_response.text
        elif hasattr(response, 'text'):
            text = response.text

        if self.step == "get_weather":
            # 保存天气信息并生成报告
            await ctx.send_message(
                AgentExecutorRequest(
                    messages=[ChatMessage(
                        role=Role.USER,
                        text=f"Create a weather report based on: {text[:100]}, better to talk a reference small joke in it"
                    )],
                    should_respond=True
                ),
                target_id="gen_script_executor"
            )
            self.step = "generate_report"
        else:
            # 输出最终报告
            await ctx.yield_output(f"""{text}""")


# ============ 设置agents ============
search_agent = setup_search_agent()
gen_script_agent = setup_gen_script_agent()

# ============ 创建executors ============
main_executor = SimpleWeatherWorkflow(id="main_executor")
search_executor = AgentExecutor(agent=search_agent, id="search_executor")
gen_script_executor = AgentExecutor(agent=gen_script_agent, id="gen_script_executor")

# ============ 构建workflow ============
workflow = (
    WorkflowBuilder()
    .set_start_executor(main_executor)
    # required steps when generate WorkflowOutputEvent during run podcast_app.py
    # skip steps when only run main.py for workflow
    .add_edge(main_executor, search_executor) 
    .add_edge(search_executor, main_executor)
    # main steps
    .add_edge(main_executor, gen_script_executor)
    .add_edge(gen_script_executor, main_executor)
    .build()

)

