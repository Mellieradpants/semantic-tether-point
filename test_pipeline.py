from pipeline.run_pipeline import run_pipeline

sample_input = """
<root>
  <section id="1">Hello world</section>
  <section id="2">Another section</section>
</root>
"""

result = run_pipeline(sample_input)

print(result)
