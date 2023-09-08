

import torch
from transformers import GPT2Tokenizer, T5ForConditionalGeneration
from peft import PeftModel, PeftConfig


base_model_name = "ai-forever/FRED-T5-1.7B"
peft_path = '/content/drive/MyDrive/PROJECTS_COMPETITIONS/digital_copy/models/den4ik-t5/out/checkpoint-40'
pre_prompt = 'Тебя зовут Никита, тебе 21 год. Ты учишься на 3-ем курсе ВШЭ и занимаешься машинным обучением. Ты общаешься со своим другом, напиши ответ на его сообщение. '


class Digital_copy:
    def __init__(self):

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = GPT2Tokenizer.from_pretrained(base_model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(
            base_model_name, load_in_8bit=True, device_map="auto")
        self.peft_config = PeftConfig.from_pretrained(peft_path)
        self.peft_trained_model = PeftModel.from_pretrained(
            self.model, peft_path, device_map="auto").eval()

    def generate(self, msg, dialog, pre_prompt=pre_prompt, temperature=0.8, num_beams=2, max_length=50):

        prompt = '<SC1>' + pre_prompt + 'Ваш прошлый диалог:' + \
            '\n'.join(dialog) + ' Твой ответ:<extra_id_0>'
        input_ids = self.tokenizer(
            prompt, return_tensors='pt').input_ids.to(self.device)
        out_ids = peft_trained_model.generate(input_ids=input_ids,
                                              max_length=max_length,
                                              eos_token_id=tokenizer.eos_token_id,
                                              early_stopping=True,
                                              do_sample=True,
                                              num_beams=num_beams,
                                              temperature=temperature,
                                              top_k=50,
                                              top_p=0.75)

        output = tokenizer.decode(out_ids[0][1:]).replace('<extra_id_0>', '')
        if '</s>' in output:
            output = t5_output[:t5_output.find('</s>')].strip()

        return output
