import { useState, useEffect } from 'react'

function App() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    // Use a URL completa do backend - IMPORTANTE!
    fetch('http://localhost:8000/api/items')
      .then(response => {
        if (!response.ok) {
          throw new Error('Erro na resposta da API')
        }
        return response.json()
      })
      .then(data => {
        setData(data)  // ← CORRIGIDO: data em vez de data.items
        setLoading(false)
      })
      .catch(error => {
        console.error('Erro ao buscar dados:', error)
        setError(error.message)
        setLoading(false)
      })
  }, [])

  if (loading) return <div>Carregando...</div>
  if (error) return <div>Erro: {error}</div>

  return (
    <div className="App">
      <h1>Meu App React com Docker</h1>
      <div>
        <h2>Itens do Banco de Dados:</h2>
        {data.length === 0 ? (
          <p>Nenhum item encontrado.</p>
        ) : (
          <ul style={{ listStyleType: 'none', }}>
            
            {data.map(item => (
              <li key={item.id}>
                <strong>{item.name}</strong> - {item.description}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

export default App