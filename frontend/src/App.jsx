import { useState, useEffect } from 'react'

function App() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/items')
      .then(response => response.json())
      .then(data => {
        setData(data.items || [])
        setLoading(false)
      })
      .catch(error => {
        console.error('Erro ao buscar dados:', error)
        setLoading(false)
      })
  }, [])

  if (loading) return <div>Carregando...</div>

  return (
    <div className="App">
      <h1>Meu App React com Docker</h1>
      <div>
        <h2>Itens do Banco de Dados:</h2>
        <ul>
          {data.map(item => (
            <li key={item.id}>{item.name} - {item.description}</li>
          ))}
        </ul>
      </div>
    </div>
  )
}

export default App