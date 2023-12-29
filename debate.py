from socrasynth_chat import AgentConfig, DebateConfig, SocraSynth_Chat
import pandas as pd

# Load subject csv
private_subjects = pd.read_csv('subjects-private.csv').values.tolist()
public_subjects = pd.read_csv('subjects-public.csv').values.tolist()

subjects = private_subjects + public_subjects

chat = SocraSynth_Chat('mcega', '212866', verbose=True)
Agent_A = AgentConfig(frequency_penalty=0.5, presence_penalty=0.5, temperature=1.5)
Agent_B = AgentConfig()
print([subject[0] for subject in subjects])

for subject in subjects[16:]:
    name, subject_title = subject
    print(f'Debating {name}')
    debate_config = DebateConfig(subject_title, Agent_A, Agent_B)
    success = False
    while not success:
        try:
            conclusion_A, conclusion_B, dialogue = chat.debate(debate_config, verbose=True)
            print(f'{name} debate completed')
        except Exception as e:
            print(f'Error while debating {name}')
            print(e)
            continue
        
        try:
            # Save raw dialogue to txt
            with open(f'dialogue/{name}.txt', 'w') as f:
                f.write(dialogue)

            # Get debate topics from conclusion dict's key
            topics = list(conclusion_A.keys())
        
            # Get debate conclusion from conclusion dict's value
            conclusion_A = list(conclusion_A.values())
            conclusion_B = list(conclusion_B.values())
        
            # Save debate conclusion to csv
            df = pd.DataFrame({'topic': topics, 'Agent-A': conclusion_A, 'Agent-B': conclusion_B})
            df.to_csv(f'output/{name}.csv', index=False)
            print(f'{name} debate conclusion saved')

        except Exception as e:
            print(f'Error while saving debate conclusion for {name}')
            print(e)
            # Save raw conclusion to txt
            with open(f'output/{name}.txt', 'w') as f:
                f.write(f'Agent-A: {conclusion_A}\n')
                f.write(f'Agent-B: {conclusion_B}\n')
            continue
        success = True