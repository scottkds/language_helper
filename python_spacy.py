import spacy
from spacy.lang.en.examples import sentences
from spacy import displacy

def lots_o_text():
    return """La historia de la salida del poder de Evo Morales es complicada. Sin duda
    hubo una rebelión popular ante el vergonzoso y torpe fraude electoral del pasado
    20 de octubre. Pero también es cierto que la explícita presión de los militares
    obligó a Morales a dejar la presidencia. Hubo fraude y hubo golpe. Las dos cosas.
    Evo cayó, fundamentalmente, por su incontrolable deseo de permanecer en el poder.
    Estos son los datos. Gana legítimamente las elecciones del 2005 -convirtiéndose
    en el primer presidente indígena en la historia moderna de Bolivia- y después
    lidera un esfuerzo para cambiar la constitución.

    Vuelve a ganar en el 2009. Pero ahí empiezan las trampas. Dice que su primer \
    período presidencial no cuenta y eso le permite buscar (y ganar) una segunda
    reelección en el 2014. No contento con quedarse en el poder hasta el 2020,
    organiza un plebiscito en el 2016 para buscar otra reelección y, en esa ocasión,
    lo pierde. Pero, mal perdedor, él asegura que ese resultado viola sus derechos.
    Va al Tribunal Constitucional, que él controla, y logra un dictamen que le permite
    reelegirse todas las veces que quiera. Otra trampa.

    Eso nos lleva a las elecciones del 20 de octubre del 2019 donde Evo buscaba
    un cuarto período presidencial. Tras una extrañísima caída del sistema por
    varias horas, el Tribunal Supremo Electoral (también dominado por Evo) lo declara
    ganador en la primera vuelta. Pero el fraude es obvio.
    Un equipo auditor de la Organización de Estados Americanos (OEA) determinó que
    hubo “manipulaciones al sistema informático”, “alteraciones y firmas falsificadas”,
    “inconsistencias con el número de ciudadanos que sufragaron” y, por lo tanto,
    “no puede validar los resultados de la presente elección”."""

nlp = spacy.load('es_core_news_sm')
doc = nlp("Eso nos lleva a las elecciones del 20 de octubre del 2019 donde Evo buscaba un cuarto período presidencial")
print(doc.text)
for token in doc:
    print(token.text, token.pos_, token.lemma_)

displacy.serve(doc, style='dep')
