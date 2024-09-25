# Benchmarking RDF.ex
# Presents as a CLI tool with 3 commands:
# Usage: executable <task> <filename>
# task: parse, query, query2

defmodule Belix do
  def main(args) do
    [task, filename] = args

    case task do
      "parse" -> parse(filename)
      "query" -> query(filename, 1)
      "query2" -> query(filename, 2)
    end
  end

  defp parse(filename) do
    start_time = :os.timestamp()
    RDF.NTriples.read_file(filename)
    end_time = :os.timestamp()
    # seconds
    elapsed_time = :timer.now_diff(end_time, start_time) / 1_000_000
    IO.puts("#{elapsed_time}")
  end

  defp query(filename, query_number) do
    mem_before = :erlang.memory(:processes)
    {time_load, {:ok, rdf}} = :timer.tc(&RDF.NTriples.read_file/1, [filename])
    mem_graph = :erlang.memory(:processes) - mem_before

    pattern =
      case query_number do
        1 -> {:_, RDF.type(), RDF.IRI.new("http://dbpedia.org/ontology/Person")}
        2 -> {RDF.IRI.new("http://dbpedia.org/resource/Vincent_Descombes_Sevoie"), :_, :_}
      end

    query = RDF.Query.bgp(pattern)
    results = RDF.Graph.query_stream(rdf, query)
    {time_first, first_match} = :timer.tc(fn -> Enum.take(results, 1) end)
    {time_all, count} = :timer.tc(fn -> Enum.count(results) end)
    time_rest = time_all - time_first

    IO.puts("matching triples: #{count}")
    IO.inspect(first_match)
    IO.puts(
      "#{time_load / 1_000_000}, #{mem_graph}, #{time_first / 1_000_000}, #{time_rest / 1_000_000}"
    )
  end
end


Belix.main(System.argv())
