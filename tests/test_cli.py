# Simple test case for the CLI
def test_main():
    from click.testing import CliRunner
    from cvtease.cli import main

    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0
    assert "This tool is under development, so be patient." in result.output
