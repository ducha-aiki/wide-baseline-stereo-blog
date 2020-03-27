FROM hamelsmu/fastpages-nbdev

WORKDIR /fastpages
COPY . .
RUN chmod u+x action_entrypoint.sh
RUN chmod u+x word2post.sh
RUN pip install jupyter_latex_envs --user
RUN pip install git+https://github.com/ducha-aiki/nbdev@latex_envs_citations --user
CMD [ "/fastpages/action_entrypoint.sh" ]
