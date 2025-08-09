<!-- AUTO-GENERATED README - DO NOT EDIT DIRECTLY -->
<!-- Generated at {{ now }} UTC -->

<p align="center">
  <img src="assets/banner.gif" width="100%" alt="Balaji Chowdary Banner">
</p>

<h1 align="center">Hi 👋, I'm Balaji Chowdary</h1>
<p align="center">CSE Student • Full Stack Dev • AI/ML Enthusiast</p>

---

## Live Snapshot
- GitHub: `{{ username }}`
- Updated: `{{ now }}` UTC

{% if leetcode.matchedUser %}
## LeetCode Stats
- Username: {{ leetcode.matchedUser.username }}
- Ranking: {{ leetcode.matchedUser.profile.ranking or '—' }}
- Reputation: {{ leetcode.matchedUser.profile.reputation or '—' }}
{% else %}
## LeetCode Stats
- Public data unavailable or LEETCODE_USERNAME not set in secrets.
{% endif %}

---

## Skills
<p align="center">
{% for name, path in skill_svgs.items() %}
  <img src="{{ path }}" alt="{{ name }} skill" />
{% endfor %}
</p>

---

## Projects
<p align="center">
<a href="https://github.com/{{ username }}/project1"><img src="assets/preview-project1.gif" width="48%"></a>
<a href="https://github.com/{{ username }}/project2"><img src="assets/preview-project2.gif" width="48%"></a>
</p>

---

## Contribution snake
<p align="center">
<img src="output/github-contribution-grid-snake.svg" alt="snake" />
</p>

---

<p align="center">
  <img src="https://komarev.com/ghpvc/?username={{ username }}&label=Profile%20views" alt="Profile views" />
</p>

*This README is generated automatically. Want different widgets? Add a new generator script in `scripts/` and update `dynamic-readme.yml`.*
