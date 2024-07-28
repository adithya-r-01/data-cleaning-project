# YesWorkflow Tool

### Dependencies

1) Java (JRE) version 1.7 or higher

2) Graphviz

3) [YesWorkflow JAR](https://github.com/yesworkflow-org/yw-prototypes/releases/download/v0.2.0/yesworkflow-0.2.0-jar-with-dependencies.jar)

### Workflow Graph Generation Command

```bash
java -jar tools/yesworkflow-0.2.0-jar-with-dependencies.jar graph AnnotatedDataCleaningChanges.py | dot -Tpng -o DataCleaningChanges.png
java -jar tools/yesworkflow-0.2.0-jar-with-dependencies.jar graph AnnotatedICViolations.py | dot -Tpng -o ICViolations.png
```
