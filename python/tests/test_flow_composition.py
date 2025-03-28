import unittest
import asyncio
from pocketflow import Node, Flow

class NumberNode(Node):
    def __init__(self, number):
        super().__init__()
        self.number = number

    async def prep(self, shared_storage):
        shared_storage['current'] = self.number

class AddNode(Node):
    def __init__(self, number):
        super().__init__()
        self.number = number
    
    async def prep(self, shared_storage):
        shared_storage['current'] += self.number
        return None

class MultiplyNode(Node):
    def __init__(self, number):
        super().__init__()
        self.number = number
    
    async def prep(self, shared_storage):
        shared_storage['current'] *= self.number
        return None

class AsyncOperationNode(Node):
    async def prep(self, shared_storage):
        await asyncio.sleep(0.01)
        shared_storage['async_ops'] = shared_storage.get('async_ops', 0) + 1
        return None

class TestFlowComposition(unittest.IsolatedAsyncioTestCase):
    async def test_flow_as_node(self):
        shared_storage = {}
        
        # Inner flow f1
        f1 = Flow(NumberNode(5))
        f1.start >> AddNode(10) >> MultiplyNode(2)

        # f2 starts with f1
        f2 = Flow(f1)

        # Wrapper flow f3
        f3 = Flow(f2)
        await f3.run(shared_storage)

        self.assertEqual(shared_storage['current'], 30)

    async def test_nested_flows(self):
        shared_storage = {}

        # Inner flow
        inner_flow = Flow(NumberNode(5))
        inner_flow.start >> AddNode(3)

        # Middle flow
        middle_flow = Flow(inner_flow)
        middle_flow.start >> MultiplyNode(4)

        # Wrapper flow
        wrapper_flow = Flow(middle_flow)
        await wrapper_flow.run(shared_storage)

        self.assertEqual(shared_storage['current'], 32)

    async def test_flow_chaining(self):
        """
        Demonstrates chaining two flows with proper wrapping:
        flow1: NumberNode(10) -> AddNode(10) # final = 20
        flow2: MultiplyNode(2) # final = 40
        wrapper_flow: contains both flow1 and flow2 to ensure proper execution
        Expected final result: (10 + 10) * 2 = 40.
        """
        shared_storage = {}

        # flow1
        numbernode = NumberNode(10)
        numbernode >> AddNode(10)
        flow1 = Flow(start=numbernode)

        # flow2
        flow2 = Flow(start=MultiplyNode(2))

        # Chain flow1 to flow2
        flow1 >> flow2

        # Wrapper flow
        wrapper_flow = Flow(flow1)
        await wrapper_flow.run(shared_storage)

        self.assertEqual(shared_storage['current'], 40)

    async def test_async_nested_flows(self):
        shared_storage = {}

        # Inner async flow
        inner_flow = Flow(AsyncOperationNode())
        inner_flow.start >> AsyncOperationNode()

        # Outer flow
        outer_flow = Flow(inner_flow)
        outer_flow.start >> AsyncOperationNode()

        await outer_flow.run(shared_storage)
        self.assertEqual(shared_storage['async_ops'], 3)

    async def test_error_propagation_in_nested_flows(self):
        class ErrorNode(Node):
            async def prep(self, shared_storage):
                raise ValueError("Nested flow error")

        shared_storage = {}

        # Inner flow with error
        inner_flow = Flow(NumberNode(5))
        inner_flow >> ErrorNode()

        # Outer flow
        outer_flow = Flow(inner_flow)
        outer_flow >> NumberNode(10)

        with self.assertRaises(ValueError):
            await outer_flow.run(shared_storage)

        # Should stop before the outer flow's NumberNode
        self.assertEqual(shared_storage['current'], 5)

if __name__ == '__main__':
    unittest.main()
