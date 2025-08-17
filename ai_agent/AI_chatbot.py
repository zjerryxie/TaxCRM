def customized_answers():
    logger = logging.getLogger("web2py.app.myapp")
    logger.setLevel(logging.DEBUG)

    try:
        question_context = request.vars.question_context
        question = request.vars.question

        logger.error( "Error inside customized_answers " )

        if question_context is not None :

            if question is not None:

                logger.error(f"inside customized_answers, question_context = {question_context}, question = {question}")

                openai_response = OpenAI(api_key="your_api_key").chat.completions.create(
                    model="your_gpt_model",
                    messages=[
                        {"role": "system", "content": str(question_context)},
                        {"role": "user", "content": str(question)}
                    ]
                )

                #answer = openai_response.choices[0].message.content.strip()
                answer_content = "begoWise advisor's answer: " + openai_response.choices[0].message.content.strip()

                logger.error(f"Inside customized_answers, type of begoWise_answers = {type(answer_content)}")

                logger.error(f"Inside customized_answers, begoWise_answers = {answer_content}")

                return response.json(dict(begoWise_answers=answer_content))

            else:

                question = "which of the above choices is correct ? please select only one and explain your reasons"

                logger.error(f"inside customized_answers, question_context = {question_context}, question = {question}")

                openai_response = OpenAI(api_key="your_api_key").chat.completions.create(
                    model="your_ai_model",
                    messages=[
                        {"role": "system", "content": str(question_context)},
                        {"role": "user", "content": str(question)}
                    ]
                )

                #answer = openai_response.choices[0].message.content.strip()
                answer_content = "begoWise advisor's answer: " + openai_response.choices[0].message.content.strip()

                logger.error(f"Inside customized_answers, type of begoWise_answers = {type(answer_content)}")

                logger.error(f"Inside customized_answers, begoWise_answers = {answer_content}")

                return response.json(dict(begoWise_answers=answer_content))


        else:
            logger.error("Error inside customized_answers, missing question_context or question")
            return response.json(dict(begoWise_answers="missing question_context or question"))

    except Exception as e:
        logger.error(f"Error in customized_answers: {str(e)}")
        return response.json(dict(begoWise_answers=f"Error: {str(e)}"))

