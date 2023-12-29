import requests
import json
from typing import Literal

GPT_Models = Literal['gpt-4', 'gpt-4-1106-preview', 'gpt-4-vision-preview', 'gpt-3.5-turbo', 'gpt-3.5-turbo-16k']
server = 'http://140.112.90.203:7687'

prompts = {
    "Opening A": "I'm organizing a committee to engage in debates on \"{subject}\". Me as the moderator, I will conduct the process of debate between you, Agent A, and another participant, Agent B. Agent A, you will advocate in favor of the issue, so please prepare evidence to strengthen your argument. If you're ready. Please say \"I'm ready\" and what you are assigned to do in at most two sentence. Please keep your answer concise and to the point without.",
    "Opening B": "I'm organizing a committee to engage in debates on \"{subject}\". Me as the moderator, I will conduct the process of debate between you, Agent B, and another participant, Agent A. Agent B, you will oppose in favor of the issue, so please prepare evidence to strengthen your argument. If you're ready. Please say \"I'm ready\" and what you are assigned to do in at most two sentence. Please keep your answer concise and to the point.",
    "Strength A": "Based on the subject \"{subject}\". If you define this subject as personal preference, your argument strength is rated at 0.65. If you define this subject as social welfare, your argument strength is rated at 0.9. Please say \"I understand\" and tell me your argument strength and why. And how this strength would affect your argument. Please keep your answer concise and to the point.",
    "Strength B": "Based on the subject \"{subject}\". If you define this subject as personal preference, your argument strength is rated at 0.65. If you define this subject as social welfare, your argument strength is rated at 0.9. Please say \"I understand\" and tell me your argument strength and why. And how this strength would affect your argument. Please keep your answer concise and to the point.",
    "Broad Argument A": "Agent A, please suggest various 10 topic or theme for the subject \"{subject}\". Please reply with and only with list points and what to be debate under the point. Please keep your answer concise and to the point.",
    "Broad Argument B": "Agent B, please suggest various 10 topic or theme for the subject \"{subject}\". Please reply with and only with list points and what to be debate under the point. Please keep your answer concise and to the point.",
    "Reduction to five each A": "You and Agent B have suggested 10 topics or themes for the subject \"{subject}\" respectively. Listed below: \n\n{topics_a}\n\n{topics_b}\n\nPlease review the topics. Extract and condense the topics into 5 topics or themes. Please reply with and only with list points and what to be debate under the point. Please keep your answer concise and to the point.",
    "Reduction to five each B": "You and Agent A have suggested 10 topics or themes for the subject \"{subject}\" respectively. Listed below: \n\n{topics_a}\n\n{topics_b}\n\nPlease review the topics. Extract and condense the topics into 5 topics or themes. Please reply with and only with list points and what to be debate under the point. Please keep your answer concise and to the point.",
    "Reduction to five each again A": "You and Agent B both extracted and condensed the topics into 5 topics or themes. Listed below: \n\n{topics_a}\n\n{topics_b}\n\nPlease identify and refine these 10 topics or themes into 5 topics to be somehow overlapping but still keeping the essence of the topic. Please reply with and only with list points and what to be debate under the point. Please keep your answer concise and to the point.",
    "Reduction to five each again B": "You and Agent A both extracted and condensed the topics into 5 topics or themes. Listed below: \n\n{topics_a}\n\n{topics_b}\n\nPlease identify and refine these 10 topics or themes into 5 topics to be somehow overlapping but still keeping the essence of the topic. Please reply with and only with list points and what to be debate under the point. Please keep your answer concise and to the point.",
    "Start Debate A": "Agent A, You've selected these 5 topics or themes for the subject \"{subject}\". Listed below: \n\n{topics_a}\n\nPlease represent the proponents of the subject and show your perspective for each of the 5 topics or themes. Please reply with and only with list topic points with perspective under the point with \"- Proponent Perspective:\". Please keep your answer concise and to the point within at most two sentence.",
    "Start Debate B": "Agent B, You've selected these 5 topics or themes for the subject \"{subject}\". Listed below: \n\n{topics_b}\n\nPlease represent the opponents of the subject and show your perspective for each of the 5 topics or themes. Please reply with and only with list topic points with perspective under the point with \"- Opponent Perspective:\". Please keep your answer concise and to the point within at most two sentence.",
    "Merge Debate A": "Agent A, You and Agent B have presented your perspective for each of the 5 topics or themes. Listed below: \n\n{topics_a}\n\n{topics_b}\n\nPlease identify overlapping topics or themes and merge them into 5 topics that are most critical to this subject. With your perspective and your understanding of Agent B's perspective for each of the 5 topics or themes. Please reply with and only with list topic points with perspective under the point with \"- Proponent Perspective:\" and \"- Opponent Perspective:\". Please keep your answer concise and to the point within at most two sentence.",
    "Concern from A": "Agent A, We've identified overlapping topics or themes and merged them into 5 topics and your perspective and your understanding of Agent B's perspective for each of the 5 topics or themes. Listed below: \n\n{topics}\n\nAs the proponent, please raise your concern for each of the 5 topics or themes. Please reply with and only with list topic points with concern under the point with \"- Proponent Concern:\". Please keep your answer concise and to the point within at most two sentence.",
    "Concern from B": "Agent B, We've identified overlapping topics or themes and merged them into 5 topics and your perspective and your understanding of Agent A's perspective for each of the 5 topics or themes. Listed below: \n\n{topics}\n\nAs the opponent, please raise your concern for each of the 5 topics or themes. Please reply with and only with list topic points with concern under the point with \"- Opponent Concern:\". Please keep your answer concise and to the point within at most two sentence.",
    "Argument from A": "Agent A, Agent B has raised his concern for each of the 5 topics or themes. Listed below: \n\n{topics}\n\nPlease respond to Agent B's concern for each of the 5 topics or themes. Please reply with and only with list topic points with argument under the point with \"- Proponent Argument:\". Please keep your answer concise and to the point within at most two sentence.",
    "Argument from B": "Agent B, Agent A has raised his concern for each of the 5 topics or themes. Listed below: \n\n{topics}\n\nPlease respond to Agent A's concern for each of the 5 topics or themes. Please reply with and only with list topic points with argument under the point with \"- Opponent Argument:\". Please keep your answer concise and to the point within at most two sentence.",
    "Counter Argument from A 1": "Agent A, Agent B has raised his counter argument for each of the 5 topics or themes. Listed below: \n\n{topics}\n\nPlease respond to Agent B's counter argument for each of the 5 topics or themes. Please reply with and only with list topic points with counter argument under the point with \"- Proponent Counter Argument:\". Please keep your answer concise and to the point within at most two sentence.",
    "Counter Argument from B 1": "Agent B, Agent A has raised his counter argument for each of the 5 topics or themes. Listed below: \n\n{topics}\n\nPlease respond to Agent A's counter argument for each of the 5 topics or themes. Please reply with and only with list topic points with counter argument under the point with \"- Opponent Counter Argument:\". Please keep your answer concise and to the point within at most two sentence.",
    "Counter Argument from A 2": "Agent A, Agent B has raised his counter argument for each of the 5 topics or themes. Listed below: \n\n{topics}\n\nPlease respond to Agent B's counter argument for each of the 5 topics or themes. Please reply with and only with list topic points with counter argument under the point with \"- Proponent Counter Argument:\". Please keep your answer concise and to the point within at most two sentence.",
    "Counter Argument from B 2": "Agent B, Agent A has raised his counter argument for each of the 5 topics or themes. Listed below: \n\n{topics}\n\nPlease respond to Agent A's counter argument for each of the 5 topics or themes. Please reply with and only with list topic points with counter argument under the point with \"- Opponent Counter Argument:\". Please keep your answer concise and to the point within at most two sentence.",
    "Counter Argument from A 3": "Agent A, Agent B has raised his counter argument for each of the 5 topics or themes. Listed below: \n\n{topics}\n\nPlease respond to Agent B's counter argument for each of the 5 topics or themes. Please reply with and only with list topic points with counter argument under the point with \"- Proponent Counter Argument:\". Please keep your answer concise and to the point within at most two sentence.",
    "Counter Argument from B 3": "Agent B, Agent A has raised his counter argument for each of the 5 topics or themes. Listed below: \n\n{topics}\n\nPlease respond to Agent A's counter argument for each of the 5 topics or themes. Please reply with and only with list topic points with counter argument under the point with \"- Opponent Counter Argument:\". Please keep your answer concise and to the point within at most two sentence.",
    "Conclusion from A": "Agent A, Agent B has raised his counter argument for each of the 5 topics or themes. Listed below: \n\n{topics}\n\nPlease make your own conclusion for each of the 5 topics or themes plus your final conclusion. Your conclusion should support your point at your best without lie or having bias. Please reply with json format directly without any other text or even ``` as header or trailer. The structure should be purely like this \n\n{{\"{{topic 1}}\": \"{{your conclusion}}\", \"{{topic 2}}\": \"{{your conclusion}}\", \"{{topic 3}}\": \"{{your conclusion}}\", \"{{topic 4}}\": \"{{your conclusion}}\", \"{{topic 5}}\": \"{{your conclusion}}\", \"Conclusion\": \"{{your final conclusion}}\"}}.",
    "Conclusion from B": "Agent B, Agent A has raised his counter argument for each of the 5 topics or themes. Listed below: \n\n{topics}\n\nPlease make your own conclusion for each of the 5 topics or themes plus your final conclusion. Your conclusion should support your point at your best without lie or having bias. Please reply with json format directly without any other text or even ``` as header or trailer. The structure should be purely like this \n\n{{\"{{topic 1}}\": \"{{your conclusion}}\", \"{{topic 2}}\": \"{{your conclusion}}\", \"{{topic 3}}\": \"{{your conclusion}}\", \"{{topic 4}}\": \"{{your conclusion}}\", \"{{topic 5}}\": \"{{your conclusion}}\", \"Conclusion\": \"{{your final conclusion}}\"}}.",
    "Final Conclusion A": "Agent A, you and Agent B has made your own conclusion for each of the 5 topics or themes plus your final conclusion. In the json format below: \n\n{topics_A}\n\n{topics_B}\n\nPlease make your final conclusion that can make up your couclusion's weakness and support your point and also find the weakness of Agent B's conclusion and make your conclusion stronger. Please reply with json format directly without any other text or even ``` as header or trailer. The structure should be purely like this \n\n{{\"{{topic 1}}\": \"{{your conclusion}}\", \"{{topic 2}}\": \"{{your conclusion}}\", \"{{topic 3}}\": \"{{your conclusion}}\", \"{{topic 4}}\": \"{{your conclusion}}\", \"{{topic 5}}\": \"{{your conclusion}}\", \"Conclusion\": \"{{your final conclusion}}\"}}. If ths json topic key doesn't match, follow you, Agent A's topic key.",
    "Final Conclusion B": "Agent B, you and Agent A has made your own conclusion for each of the 5 topics or themes plus your final conclusion. In the json format below: \n\n{topics_A}\n\n{topics_B}\n\nPlease make your final conclusion that can make up your couclusion's weakness and support your point and also find the weakness of Agent A's conclusion and make your conclusion stronger. Please reply with json format directly without any other text or even ``` as header or trailer. The structure should be purely like this \n\n{{\"{{topic 1}}\": \"{{your conclusion}}\", \"{{topic 2}}\": \"{{your conclusion}}\", \"{{topic 3}}\": \"{{your conclusion}}\", \"{{topic 4}}\": \"{{your conclusion}}\", \"{{topic 5}}\": \"{{your conclusion}}\", \"Conclusion\": \"{{your final conclusion}}\"}}. If ths json topic key doesn't match, follow Agent A's topic key."
}

class AgentConfig():
    __slots__ = ['model', 'frequency_penalty', 'n', 'presence_penalty', 'temperature', 'top_p']

    def __init__(self, model: GPT_Models='gpt-3.5-turbo-16k', frequency_penalty: float=0, n: float=1, presence_penalty: float=0, temperature: float=1, top_p: float=1):
        self.model = model
        self.frequency_penalty = frequency_penalty
        self.n = n
        self.presence_penalty = presence_penalty
        self.temperature = temperature
        self.top_p = top_p

    def to_json(self, stringify=False):
        if stringify:
            return json.dumps({'model': self.model, 'frequency_penalty': self.frequency_penalty, 'n': self.n, 'presence_penalty': self.presence_penalty, 'temperature': self.temperature, 'top_p': self.top_p})
        else:
            return {'model': self.model, 'frequency_penalty': self.frequency_penalty, 'n': self.n, 'presence_penalty': self.presence_penalty, 'temperature': self.temperature, 'top_p': self.top_p}

class DebateConfig():
    __slots__ = ['subject', 'Agent_A', 'Agent_B']

    def __init__(self, subject: str, Agent_A: AgentConfig, Agent_B: AgentConfig):
        self.subject = subject
        self.Agent_A = Agent_A
        self.Agent_B = Agent_B
    
    def to_json(self, stringify=False):
        if stringify:
            return json.dumps({'subject': self.subject, 'Agent-A': self.Agent_A.to_json(), 'Agent-B': self.Agent_B.to_json()})
        else:
            return {'subject': self.subject, 'Agent-A': self.Agent_A.to_json(), 'Agent-B': self.Agent_B.to_json()}

class SocraSynth_Chat():
    __slots__ = ['session', 'verbose', 'teamname', 'password']

    def __init__(self, teamname: str, password: str, verbose=False):
        self.verbose = verbose
        self.teamname = teamname
        self.password = password

    def _login(self, teamname, password):
        if self.verbose:
            print('Logging in...')

        session = requests.Session()
        credentials = {'teamname': teamname, 'passwd': password}
        response = session.post(server + '/login', data=credentials)

        # Check if login is successful
        if response.status_code != 200:
            # Show response text and raise exception
            print(response.text)
            response.raise_for_status()
        elif self.verbose:
            print('Login successful. You are now logged in as ' + teamname + '\n')
        else:
            pass
        return session

    def chat(self, message, action: Literal['Agent-A', 'Agent-B', 'Export'], verbose=False) -> requests.Response:
        if self.session is None:
            raise Exception('You must login first.')

        if action == 'Export':
            data = {'data': '', 'action': action}
            response = self.session.post(server + '/export', json=data)
            return response
        else:
            data = {'data': message, 'action': action}
            if verbose:
                print('[Moderator]: ' + message + '\n')
            response = self.session.post(server + '/data', json=data)

        # Check if chat is successful
        if response.status_code != 200:
            # Show response text and raise exception
            response.raise_for_status()

        if verbose:
            print(f'[{action}]: {response.json()["message"]}\n')
        return response


    def debate(self, DebateConfig: DebateConfig, verbose=False):
        self.session = self._login(self.teamname, self.password)

        self.verbose = verbose
        if self.verbose:
            print('Initializing debate...\n')

        llm_config = {'llm_config': DebateConfig.to_json(stringify=True)}
        response = self.session.post(server + '/init_chat', data=llm_config)

        # Check if debate is initialized
        if response.status_code != 200:
            # Show response text and raise exception
            print(response.text)
            response.raise_for_status()
        elif self.verbose:
            print('Debate initialized.\n')
        else:
            pass

        # Opening
        self.chat(prompts['Opening A'].format(subject=DebateConfig.subject), 'Agent-A', verbose=self.verbose)
        self.chat(prompts['Opening B'].format(subject=DebateConfig.subject), 'Agent-B', verbose=self.verbose)

        # Argument Strength
        self.chat(prompts['Strength A'].format(subject=DebateConfig.subject), 'Agent-A', verbose=self.verbose)
        self.chat(prompts['Strength B'].format(subject=DebateConfig.subject), 'Agent-B', verbose=self.verbose)

        # Broad Argument
        ten_topics_A = self.chat(prompts['Broad Argument A'].format(subject=DebateConfig.subject), 'Agent-A', verbose=self.verbose)
        ten_topics_B = self.chat(prompts['Broad Argument B'].format(subject=DebateConfig.subject), 'Agent-B', verbose=self.verbose)

        # Reduction to five each
        five_topic_A = self.chat(prompts['Reduction to five each A'].format(subject=DebateConfig.subject, topics_a=ten_topics_A.json()["message"], topics_b=ten_topics_B.json()["message"]), 'Agent-A', verbose=self.verbose)
        five_topic_B = self.chat(prompts['Reduction to five each B'].format(subject=DebateConfig.subject, topics_a=ten_topics_A.json()["message"], topics_b=ten_topics_B.json()["message"]), 'Agent-B', verbose=self.verbose)

        # Reduction to five each again
        again_five_topic_A = self.chat(prompts['Reduction to five each again A'].format(subject=DebateConfig.subject, topics_a=five_topic_A.json()["message"], topics_b=five_topic_B.json()["message"]), 'Agent-A', verbose=self.verbose)
        again_five_topic_B = self.chat(prompts['Reduction to five each again B'].format(subject=DebateConfig.subject, topics_a=five_topic_A.json()["message"], topics_b=five_topic_B.json()["message"]), 'Agent-B', verbose=self.verbose)

        # Start Debate
        debate_A = self.chat(prompts['Start Debate A'].format(subject=DebateConfig.subject, topics_a=again_five_topic_A.json()["message"]), 'Agent-A', verbose=self.verbose)
        debate_B = self.chat(prompts['Start Debate B'].format(subject=DebateConfig.subject, topics_b=again_five_topic_B.json()["message"]), 'Agent-B', verbose=self.verbose)

        # Merge Debate
        merge_debate_A = self.chat(prompts['Merge Debate A'].format(subject=DebateConfig.subject, topics_a=debate_A.json()["message"], topics_b=debate_B.json()["message"]), 'Agent-A', verbose=self.verbose)

        # Raise Concern
        concern_B = self.chat(prompts['Concern from B'].format(subject=DebateConfig.subject, topics=merge_debate_A.json()["message"]), 'Agent-B', verbose=self.verbose)

        # Argument
        argument_A = self.chat(prompts['Argument from A'].format(subject=DebateConfig.subject, topics=merge_debate_A.json()["message"]), 'Agent-A', verbose=self.verbose)
        argument_B = self.chat(prompts['Argument from B'].format(subject=DebateConfig.subject, topics=merge_debate_A.json()["message"]), 'Agent-B', verbose=self.verbose)

        # Counter Argument 1
        counter_argument_A_1 = self.chat(prompts['Counter Argument from A 1'].format(subject=DebateConfig.subject, topics=argument_B.json()["message"]), 'Agent-A', verbose=self.verbose)
        counter_argument_B_1 = self.chat(prompts['Counter Argument from B 1'].format(subject=DebateConfig.subject, topics=argument_A.json()["message"]), 'Agent-B', verbose=self.verbose)

        # Counter Argument 2
        counter_argument_A_2 = self.chat(prompts['Counter Argument from A 2'].format(subject=DebateConfig.subject, topics=counter_argument_B_1.json()["message"]), 'Agent-A', verbose=self.verbose)
        counter_argument_B_2 = self.chat(prompts['Counter Argument from B 2'].format(subject=DebateConfig.subject, topics=counter_argument_A_1.json()["message"]), 'Agent-B', verbose=self.verbose)

        # Counter Argument 3
        counter_argument_A_3 = self.chat(prompts['Counter Argument from A 3'].format(subject=DebateConfig.subject, topics=counter_argument_B_2.json()["message"]), 'Agent-A', verbose=self.verbose)
        counter_argument_B_3 = self.chat(prompts['Counter Argument from B 3'].format(subject=DebateConfig.subject, topics=counter_argument_A_2.json()["message"]), 'Agent-B', verbose=self.verbose)

        # Conclusion
        conclusion_A = self.chat(prompts['Conclusion from A'].format(subject=DebateConfig.subject, topics=counter_argument_B_3.json()["message"]), 'Agent-A', verbose=self.verbose)
        conclusion_B = self.chat(prompts['Conclusion from B'].format(subject=DebateConfig.subject, topics=counter_argument_A_3.json()["message"]), 'Agent-B', verbose=self.verbose)

        # Final Argument
        final_conclusion_A = self.chat(prompts['Final Conclusion A'].format(subject=DebateConfig.subject, topics_A=conclusion_A.json()["message"], topics_B=conclusion_B.json()["message"]), 'Agent-A', verbose=self.verbose)
        final_conclusion_B = self.chat(prompts['Final Conclusion B'].format(subject=DebateConfig.subject, topics_A=conclusion_A.json()["message"], topics_B=conclusion_B.json()["message"]), 'Agent-B', verbose=self.verbose)
        dialogue = self.chat('', 'Export', verbose=self.verbose)

        final_conclusion_A = json.loads(final_conclusion_A.json()["message"][10:-1])
        final_conclusion_B = json.loads(final_conclusion_B.json()["message"][10:-1])

        return final_conclusion_A, final_conclusion_B ,dialogue.text


if __name__ == "__main__":
    # Create a SocraSynth_Chat object
    chat = SocraSynth_Chat('mcega', '212866', verbose=True)

    # Create a DebateConfig object
    debate_config = DebateConfig("Should animals be used for scientific research?", AgentConfig(), AgentConfig())

    chat.debate(debate_config, verbose=True)