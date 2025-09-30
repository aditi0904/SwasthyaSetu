import json
import pytest
from sih.ayush import fetch_who_data, generate_fhir

def test_sync_terms(monkeypatch):
    # Mock WHO API response
    fake_response = {
        "destinationEntities": [
            {"id": "12345", "title": "Fake ICD Entity"}
        ]
    }

    def mock_get_entities(*args, **kwargs):
        return fake_response["destinationEntities"]

    # Patch WHO fetcher
    monkeypatch.setattr(fetch_who_data, "get_entities", mock_get_entities)

    entities = fetch_who_data.sync_terms()
    assert len(entities) > 0
    assert entities[0]["id"] == "12345"

def test_merge_into_conceptmap(tmp_path):
    # Minimal conceptmap stub
    conceptmap = {
        "resourceType": "ConceptMap",
        "group": [{"element": []}]
    }
    entities = [{"id": "12345", "title": "Fake ICD Entity"}]

    updated = fetch_who_data.merge_entities_into_conceptmap(conceptmap, entities)

    assert len(updated["group"][0]["element"]) > 0
    assert updated["group"][0]["element"][0]["target"][0]["code"] == "12345"
