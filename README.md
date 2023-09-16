<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<!-- [![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url] -->



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/tttonyalpha/digital_copy">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">My digital doppelganger</h3>

  <p align="center">
    I fine-tuned a LLM using free Google Colab on my Telegram conversations and created my digital doppelganger.
    <br />
    <a href="https://github.com/tttonyalpha/digital_copy"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/tttonyalpha/digital_copy">View Demo</a>
    ·
    <a href="https://github.com/tttonyalpha/digital_copy/issues">Report Bug</a>
    ·
    <a href="https://github.com/tttonyalpha/digital_copy/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<!-- <details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>
 -->


<!-- ABOUT THE PROJECT -->
## About The Project

https://github.com/tttonyalpha/digital_copy/assets/79598074/26b72c19-90f3-409c-99dc-f6cef7a46ef9


<!-- ![Dialogue screenshot][product-screenshot]  -->
<!-- (https://drive.google.com/file/d/12k2PHKTiuc_fPejNALLAS7gnQKYj06X2/view?usp=sharing) -->

This is a conversational model that imitates mе. As the base model I took [FRED-T5-1.7B](https://huggingface.co/ai-forever/FRED-T5-1.7B) - SOTA Russian LLM released 2 month ago - and fine-tuned it using instruct tuning on a dataset of 30k my Telegram conversations. I added a knowledge base with facts about me and a user feedback system with model fine-tuning on positive examples


## Data collection and preparation

I exported selected dialogues from my two Telegram accounts in JSON format. Then, using the script tg_dump_parser.py, I filtered messages by removing links and messages with a large number of characters, and created samples for training. Each sample consists of a context in which the dialogue occur and my response . The context is a set of messages that are within a specific time frame, in my case, I chose 3 hours. In order not to lose generation quality and to speed-up the training process, I decided to limit the context length to 500 characters and the length of each individual message to 200 characters

![Picsart_23-09-16_16-45-58-188 (2)](https://github.com/tttonyalpha/digital_copy/assets/79598074/91fdfa51-051c-439e-9d08-89a39f0bf1ed)


## Model selection 

For my task, I tried out several models in few-shot mode: falcon-7B, llama-2-7B, ruDialoGPT, rugpt3_based_on_gpt2, ruGPT-3.5-13B, FRED-T5-1.7B. Due to limited computational resources, time constraints, and the availability of Russian language among the models, FRED-T5 performed the best. Even in its pre-trained version, it understood instructions well and could maintain a sufficiently large context. Additionally, my choice is confirmed by the [Russian SuperGLUE Leaderboard](https://russiansuperglue.com/leaderboard/2)

![image](https://github.com/tttonyalpha/digital_copy/assets/79598074/441ce490-3577-4834-b093-cef7f67990eb)


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Efficient FRED-T5 fine-tuning 

#### 8-bit Quantization, LoRA and GPU memory optimization

I had 6 free versions of Google Colab with an NVIDIA T4 GPU(16GB) and 12GB of RAM. In order to fit the model into such a small memory space, I used a quantized to int8 model. Yes, this caused a decrease in the speed of arithmetic operations, but it allowed me to fit larger models on the GPU.

To speed up the training process, I decided to use LoRA [[2]](#2). Now, instead of training the entire weight matrix, I trained low rank supplement, which significantly reduced the training time without a significant loss of quality

I also used gradient checkpointing and gradient accumulation to save GPU memory and increase effective batch size.


#### Fine-tuning process 

It takes 19 hours to finetune the model on a single T4 GPU. Due to free Google Colab limitations, I had to save checkpoints of the model every 20 iterations and used 6 Google accounts

[see fine-tuning notebooks](https://github.com/tttonyalpha/digital_copy/tree/main/models_traning)

![filename](https://github.com/tttonyalpha/digital_copy/assets/79598074/d8ecbd3f-2405-4fe0-aa82-f030096c7bd1)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ## Feature 3: Activity recognition on images 
  
If I haven't filled out the report, but attached photos, bot automatically analyzes the images and recognizes activities -->


<!-- 

### Built With

* [![Next][Next.js]][Next-url]
* [![React][React.js]][React-url]
* [![Vue][Vue.js]][Vue-url]
* [![Angular][Angular.io]][Angular-url]
* [![Svelte][Svelte.dev]][Svelte-url]
* [![Laravel][Laravel.com]][Laravel-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url] -->

<!-- <p align="right">(<a href="#readme-top">back to top</a>)</p>
 -->


<!-- ROADMAP -->
<!-- ## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



## Project structure

The project has the following structure:
- `digital_copy/app`: Flask app for model 
- `digital_copy/models_traning`: `.py` scripts with model fine-tuning  
- `digital_copy/telegram_bot`: Telegram bot scripts and Dockerfile for conterization  
- `digital_copy/telegram_bot_for_debug`: light version of telegram bot for debug
- `digital_copy/tg_dump_parser.py`: telegram gualogues dump parser 

## How to run

#### Google Colab version 


1. Insert bot token in notebook and run all cells [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1kDaW-x9D0AJjTdoWnpkkI3EC4vi6nN_X?usp=sharing)


#### Full version

1. Insert bot token in [bot.py](https://github.com/tttonyalpha/digital_copy/blob/main/telegram_bot/bot.py) 
2. From ```app``` run

```
docker-compose up --build
```

#### Debug version

1. In [tg_bot_beta.py](https://github.com/tttonyalpha/digital_copy/blob/main/telegram_bot_for_debug/tg_bot_beta.py) replace ```'BOT_TOKEN'``` with your bot token 
2. Download model's checkpoint 
3. In [tg_bot_beta.py](https://github.com/tttonyalpha/digital_copy/blob/main/telegram_bot_for_debug/tg_bot_beta.py) replace ```'PATH_TO_CHECKPOINT'``` and ```'KNOWLEDGE_BASE_PATH'``` with it's actual path
4. Inside ```telegram_bot_for_debug``` run: 

```
docker-compose up --build
```


<!-- ROADMAP -->
## Roadmap

- [x] Telegram dialogues parser
- [x] Dialogue model based on FRED-T5
- [x] Flask server and Telegram bot
- [x] Textual knowledge retriever


- [ ] Add SSA metric
- [ ] Finetuning system based on human feedback 
- [ ] RLHF



<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contacts

Telegram: [@my_name_is_nikita_hey](https://t.me/my_name_is_nikita_hey) <br>
Mail: tttonyalpha@gmail.com 



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.


## References

<a id="1">[1]</a> 
Towards a Human-like Open-Domain Chatbot.
Daniel Adiwardana, Minh-Thang Luong, David R. So, Jamie Hall, Noah Fiedel, Romal Thoppilan, Zi Yang, Apoorv Kulshreshtha, Gaurav Nemade, Yifeng Lu, Quoc V. Le<br>
[arXiv:2001.09977](https://arxiv.org/abs/2001.09977)

<a id="2">[2]</a> 
LoRA: Low-Rank Adaptation of Large Language Models
Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen <br>
[arXiv:2106.09685](https://arxiv.org/abs/2106.09685)

<a id="3">[3]</a> 
Training language models to follow instructions with human feedback
Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul Christiano, Jan Leike, Ryan Lowe<br>
[arXiv:2203.02155](https://arxiv.org/abs/2203.02155)

<a id="4">[4]</a> 
Scaling Instruction-Finetuned Language Models.
Team from Google.<br>
[arXiv:2210.11416](https://arxiv.org/abs/2210.11416)

<a id="5">[5]</a> 
Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.
Nils Reimers, Iryna Gurevych. <br>
[arXiv:1908.10084](https://arxiv.org/abs/1908.10084)






<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/channel_screen.png
[lstm_predictions]: images/lstm_predictions.png
[lstm_recsys]: images/lstm_recsys.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
