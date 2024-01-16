cwlVersion: v1.0
$namespaces:
  s: https://schema.org/
schemas:
  - http://schema.org/version/9.0/schemaorg-current-http.rdf
s:softwareVersion: 0.0.1

$graph:
  # Workflow entrypoint
  - class: Workflow
    id: main
    label: convert or scale url image or netcdf file
    doc: Applies scale value to each pixel in a netcdf file
    inputs:
      fn:
        type: string
      input_reference:
        type: File
      size:
        type: string
    outputs:
      - id: results
        type: Directory
        outputSource:
          - convert/results
    steps:
      convert:
        run: '#convert'
        in:
          fn: fn
          input_reference: input_reference
          size: size
        out:
          - results


  - class: CommandLineTool
    id: convert
    #baseCommand: ['python', '-m', 'convert_image']
    inputs:
      fn:
        type: string
        inputBinding:
          position: 1
      input_reference:
        type: File
        inputBinding:
          position: 2
          prefix: --file
      size:
        type: string
        inputBinding:
          position: 3
    outputs:
      results:
        type: Directory
        outputBinding:
          glob: .
    requirements:
      DockerRequirement:
        dockerPull: tjellicoetpzuk/convert_nc_basic:latest
