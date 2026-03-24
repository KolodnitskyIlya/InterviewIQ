## Предполагаемая структура папок

Featured-sliced Design:

```text
app/
  app.ts
  app.css

  app/
    navigation/
    providers/

  pages/
    welcome/
    how-it-works/
    personalize/
    sign-up/
    sign-in/
    home/
    practice/
    testing/
    testing-analytics/
    analytics/
    profile/
    settings/

  widgets/
    bottom-navigation/
    progress-card/
    improvement-list/
    recent-sessions/
    category-picker/
    difficulty-picker/
    timer-picker/
    question-card/
    score-summary/
    skills-chart/

  features/
    onboarding-complete/
    choose-skill-level/
    sign-up-by-email/
    sign-in-by-email/
    start-practice/
    submit-answer/
    finish-session/
    open-settings/

  entities/
    user/
    practice/
    question/
    session/
    analytics/
    settings/

  shared/
    ui/
    api/
    lib/
    constants/
    types/
```

## Правила папок FSD

- `pages` содержит целые экраны приложения.
- `widgets` содержит крупные переиспользуемые блоки экранов. Опциональный слой, который связывает сущности и фичи. Он помогает собрать готовый смысловой блок из разных элементов.
- `features` слой для элементов кода, которые определяют, как пользователь взаимодействует с бизнес-логикой. Содержит пользовательские действия и сценарии. Это различные кнопки, выпадающие меню, селекты и всё остальное, что несёт бизнесовую логику и с чем можно взаимодействовать.
- `entities` слой для конкретных бизнес-сущностей. Например, для приложения социальной сети это будут:
  пользователь, пост, комментарий.
- `shared` слой для абстрактного, переиспользуемого кода. Содержит переиспользуемый UI, api clients, constants, helpers и types. Это могут быть иконки, отображение кнопок, вспомогательные функции и утилиты, которые неоднократно применяются в разных местах приложения.
- `app/app` самый верхний, инициализирующий слой. Он содержит корневой компонент, глобальные типы, стили, стейт и оборачивает приложение в провайдеры и контексты - то, что присуще проекту в общем.
