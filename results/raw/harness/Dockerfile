# Harness container: the model under test runs Bash with no approval prompt, so the repository is
# copied in and nothing from the host is mounted. Build from the repository root:
#   git archive --format=tar HEAD | gzip > /tmp/mtg.tgz   (or whatever ref you measure)
#   docker build -f results/raw/harness/Dockerfile -t mtg-harness --build-arg SRC=/tmp/mtg.tgz .
# Authenticate inside the container with your own Claude Code login (for example
# `docker run -it -e CLAUDE_CODE_OAUTH_TOKEN=... mtg-harness` from `claude setup-token`, or `claude login`
# in an interactive shell), then: results/raw/harness/run_control.sh. Copy results out with docker cp.
FROM node:22-bookworm-slim
ARG CC_VERSION=2.1.295
RUN apt-get update && apt-get install -y --no-install-recommends python3 git bc ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && npm install -g @anthropic-ai/claude-code@${CC_VERSION}
RUN useradd -m runner
USER runner
WORKDIR /home/runner/mind-the-gap
COPY --chown=runner:runner repo.tgz /tmp/repo.tgz
RUN tar xzf /tmp/repo.tgz && rm /tmp/repo.tgz && git init -q && git add -A && git -c user.email=h@x -c user.name=h commit -qm snapshot
ENV EVAL_SCRATCH=/home/runner/scratch
CMD ["bash"]
