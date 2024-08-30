import { describe, it, expect } from 'vitest'
import request from 'supertest'

const api = 'http://localhost:5000'

describe("api", () => {
  it('/upload post', async () => {
    const res = await request(api)
      .post('/transcrever')
      .attach("file", `${__dirname}/videoTeste.mp4`)

    expect(res.body).toMatchObject({
      text: 'rapazes vamos começar a contar uma linda história parece que vai ser uma aventura e tanto diário de bordo fotos músicas e Animação coloque trecho para retrospectiva rico parece que temos um lindo trabalho para fazer vamos fazer uma linda retrospectiva animada é capaz do recruta não sobreviver simbora'
    })

  }, 20000)

  it('/ get', async () => {

    const { body } = await request(api)
      .get('/')

    expect(body).toMatchObject({ api: 'Api test transcrição' })
  })
})