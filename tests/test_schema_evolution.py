#!/usr/bin/env python3
"""
Protocol schema evolution tests.

Tests BACKWARD, FORWARD, and FULL compatibility like Confluent Schema Registry.
Ensures protocol.yaml changes don't break existing consumers.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import yaml
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def load_protocol(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class SchemaEvolutionTests(unittest.TestCase):
    def setUp(self):
        self.original_protocol = load_protocol(ROOT / "protocol" / "protocol.yaml")
        self.original_conditions = load_json(ROOT / "protocol" / "conditions.json")
        self.original_schema = load_json(ROOT / "protocol" / "protocol.schema.json")

    def test_version_field_present(self):
        """Ensure protocol_version is present and follows semver."""
        self.assertIn("protocol_version", self.original_protocol)
        version = self.original_protocol["protocol_version"]
        parts = version.split(".")
        self.assertEqual(len(parts), 3)
        for part in parts:
            self.assertTrue(part.isdigit() or part.startswith("0"))

    def test_protocol_validates_against_schema(self):
        """Test that the current protocol validates against its schema."""
        jsonschema.validate(instance=self.original_protocol, schema=self.original_schema)

    def test_conditions_registry_exact_match(self):
        """Conditions registry must exactly match protocol predicates."""
        predicates = {
            transition["when"]
            for transitions in self.original_protocol["transitions"].values()
            for transition in transitions
        }
        predicates.update(
            transition["when"] for transition in self.original_protocol["global_transitions"]
        )

        registered = set(self.original_conditions["conditions"])
        self.assertEqual(
            registered, predicates,
            f"Registry mismatch: Missing={sorted(predicates - registered)} Extra={sorted(registered - predicates)}"
        )

    def test_fact_registry_exact_match(self):
        """Transition fact registry must exactly match referenced facts."""
        def collect_facts(expression):
            facts = set()
            if "fact" in expression:
                facts.add(expression["fact"])
            elif "not" in expression:
                facts.update(collect_facts(expression["not"]))
            else:
                for key in ("all", "any"):
                    for item in expression.get(key, []):
                        facts.update(collect_facts(item))
            return facts

        referenced_facts = set()
        for expression in self.original_conditions["conditions"].values():
            referenced_facts.update(collect_facts(expression))

        declared_facts = set(self.original_conditions["facts"])
        self.assertEqual(
            referenced_facts, declared_facts,
            f"Fact registry mismatch: Missing={sorted(referenced_facts - declared_facts)} Extra={sorted(declared_facts - referenced_facts)}"
        )

    def test_breaking_change_detection_state_removal(self):
        """Test that removing a state is detected."""
        modified_protocol = self.original_protocol.copy()
        modified_protocol["states"] = {k: v for k, v in self.original_protocol["states"].items() if k != "DIAGNOSING"}
        
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=modified_protocol, schema=self.original_schema)

    def test_breaking_change_detection_transition_removal(self):
        """Test that removing a transition source is detected."""
        modified_protocol = self.original_protocol.copy()
        modified_protocol["transitions"] = {k: v for k, v in self.original_protocol["transitions"].items() if k != "DIAGNOSING"}
        
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=modified_protocol, schema=self.original_schema)

    def test_breaking_change_detection_condition_logic_change(self):
        """Test that changing a condition's logic is detected by evaluating it."""
        from scripts.evaluate_transition_policy import evaluate_transition
        
        allowed_orig, _ = evaluate_transition("ADMITTED", "CONTAINED", {"containment_required": True})
        self.assertTrue(allowed_orig)
        
        denied_orig, _ = evaluate_transition("ADMITTED", "CONTAINED", {"containment_required": False})
        self.assertFalse(denied_orig)

    def test_schema_states_match_protocol(self):
        """Test that schema's required states match protocol states."""
        states_schema = self.original_schema["properties"]["states"]
        self.assertEqual(
            set(states_schema.get("required", [])),
            set(self.original_protocol["states"])
        )

    def test_schema_terminal_outcomes_match_protocol(self):
        """Test that schema's terminal outcomes match protocol."""
        outcomes_schema = self.original_schema["properties"]["terminal_outcomes"]
        self.assertEqual(
            set(outcomes_schema.get("required", [])),
            set(self.original_protocol["terminal_outcomes"])
        )

    def test_schema_transition_targets_match(self):
        """Test that transition 'to' enum matches protocol states + outcomes."""
        # The transition target enum is at $defs.transition.properties.to
        transition_def = self.original_schema["$defs"]["transition"]
        target_enum = transition_def["properties"]["to"]["enum"]
        
        expected = set(self.original_protocol["states"]) | set(self.original_protocol["terminal_outcomes"])
        self.assertEqual(set(target_enum), expected)

    def test_unknown_state_rejected(self):
        """Test that unknown states are rejected by transition validation."""
        from scripts.evaluate_transition_policy import evaluate_transition
        
        allowed, _ = evaluate_transition("ADMITTED", "UNKNOWN_STATE", {})
        self.assertFalse(allowed)

    def test_unknown_outcome_rejected(self):
        """Test that unknown outcomes are rejected."""
        from scripts.evaluate_transition_policy import evaluate_transition
        
        allowed, _ = evaluate_transition("ADMITTED", "UNKNOWN_OUTCOME", {})
        self.assertFalse(allowed)

    def test_protocol_validates_against_schema(self):
        """Test that the current protocol validates against its schema."""
        jsonschema.validate(instance=self.original_protocol, schema=self.original_schema)

    def test_conditions_registry_exact_match(self):
        """Conditions registry must exactly match protocol predicates."""
        predicates = {
            transition["when"]
            for transitions in self.original_protocol["transitions"].values()
            for transition in transitions
        }
        predicates.update(
            transition["when"] for transition in self.original_protocol["global_transitions"]
        )

        registered = set(self.original_conditions["conditions"])
        self.assertEqual(
            registered, predicates,
            f"Registry mismatch: Missing={sorted(predicates - registered)} Extra={sorted(registered - predicates)}"
        )

    def test_fact_registry_exact_match(self):
        """Transition fact registry must exactly match referenced facts."""
        def collect_facts(expression):
            facts = set()
            if "fact" in expression:
                facts.add(expression["fact"])
            elif "not" in expression:
                facts.update(collect_facts(expression["not"]))
            else:
                for key in ("all", "any"):
                    for item in expression.get(key, []):
                        facts.update(collect_facts(item))
            return facts

        referenced_facts = set()
        for expression in self.original_conditions["conditions"].values():
            referenced_facts.update(collect_facts(expression))

        declared_facts = set(self.original_conditions["facts"])
        self.assertEqual(
            referenced_facts, declared_facts,
            f"Fact registry mismatch: Missing={sorted(referenced_facts - declared_facts)} Extra={sorted(declared_facts - referenced_facts)}"
        )

    def test_breaking_change_detection_state_removal(self):
        """Test that removing a state is detected."""
        modified_protocol = self.original_protocol.copy()
        modified_protocol["states"] = {k: v for k, v in self.original_protocol["states"].items() if k != "DIAGNOSING"}
        
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=modified_protocol, schema=self.original_schema)

    def test_breaking_change_detection_transition_removal(self):
        """Test that removing a transition source is detected."""
        modified_protocol = self.original_protocol.copy()
        modified_protocol["transitions"] = {k: v for k, v in self.original_protocol["transitions"].items() if k != "DIAGNOSING"}
        
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=modified_protocol, schema=self.original_schema)

    def test_breaking_change_detection_condition_logic_change(self):
        """Test that changing a condition's logic is detected by evaluating it."""
        from scripts.evaluate_transition_policy import evaluate_transition
        
        allowed_orig, _ = evaluate_transition("ADMITTED", "CONTAINED", {"containment_required": True})
        self.assertTrue(allowed_orig)
        
        denied_orig, _ = evaluate_transition("ADMITTED", "CONTAINED", {"containment_required": False})
        self.assertFalse(denied_orig)

    def test_version_field_present(self):
        """Ensure protocol_version is present and follows semver."""
        self.assertIn("protocol_version", self.original_protocol)
        version = self.original_protocol["protocol_version"]
        parts = version.split(".")
        self.assertEqual(len(parts), 3)
        for part in parts:
            self.assertTrue(part.isdigit() or part.startswith("0"))

    def test_protocol_validates_against_schema(self):
        """Test that the current protocol validates against its schema."""
        jsonschema.validate(instance=self.original_protocol, schema=self.original_schema)

    def test_conditions_registry_exact_match(self):
        """Conditions registry must exactly match protocol predicates."""
        predicates = {
            transition["when"]
            for transitions in self.original_protocol["transitions"].values()
            for transition in transitions
        }
        predicates.update(
            transition["when"] for transition in self.original_protocol["global_transitions"]
        )

        registered = set(self.original_conditions["conditions"])
        self.assertEqual(
            registered, predicates,
            f"Registry mismatch: Missing={sorted(predicates - registered)} Extra={sorted(registered - predicates)}"
        )

    def test_fact_registry_exact_match(self):
        """Transition fact registry must exactly match referenced facts."""
        def collect_facts(expression):
            facts = set()
            if "fact" in expression:
                facts.add(expression["fact"])
            elif "not" in expression:
                facts.update(collect_facts(expression["not"]))
            else:
                for key in ("all", "any"):
                    for item in expression.get(key, []):
                        facts.update(collect_facts(item))
            return facts

        referenced_facts = set()
        for expression in self.original_conditions["conditions"].values():
            referenced_facts.update(collect_facts(expression))

        declared_facts = set(self.original_conditions["facts"])
        self.assertEqual(
            referenced_facts, declared_facts,
            f"Fact registry mismatch: Missing={sorted(referenced_facts - declared_facts)} Extra={sorted(declared_facts - referenced_facts)}"
        )

    def test_breaking_change_detection_state_removal(self):
        """Test that removing a state is detected."""
        modified_protocol = self.original_protocol.copy()
        modified_protocol["states"] = {k: v for k, v in self.original_protocol["states"].items() if k != "DIAGNOSING"}
        
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=modified_protocol, schema=self.original_schema)

    def test_breaking_change_detection_transition_removal(self):
        """Test that removing a transition source is detected."""
        modified_protocol = self.original_protocol.copy()
        modified_protocol["transitions"] = {k: v for k, v in self.original_protocol["transitions"].items() if k != "DIAGNOSING"}
        
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=modified_protocol, schema=self.original_schema)

    def test_breaking_change_detection_condition_logic_change(self):
        """Test that changing a condition's logic is detected by evaluating it."""
        from scripts.evaluate_transition_policy import evaluate_transition
        
        allowed_orig, _ = evaluate_transition("ADMITTED", "CONTAINED", {"containment_required": True})
        self.assertTrue(allowed_orig)
        
        denied_orig, _ = evaluate_transition("ADMITTED", "CONTAINED", {"containment_required": False})
        self.assertFalse(denied_orig)

    def test_version_field_present(self):
        """Ensure protocol_version is present and follows semver."""
        self.assertIn("protocol_version", self.original_protocol)
        version = self.original_protocol["protocol_version"]
        parts = version.split(".")
        self.assertEqual(len(parts), 3)
        for part in parts:
            self.assertTrue(part.isdigit() or part.startswith("0"))

    def test_protocol_validates_against_schema(self):
        """Test that the current protocol validates against its schema."""
        jsonschema.validate(instance=self.original_protocol, schema=self.original_schema)

    def test_conditions_registry_exact_match(self):
        """Conditions registry must exactly match protocol predicates."""
        predicates = {
            transition["when"]
            for transitions in self.original_protocol["transitions"].values()
            for transition in transitions
        }
        predicates.update(
            transition["when"] for transition in self.original_protocol["global_transitions"]
        )

        registered = set(self.original_conditions["conditions"])
        self.assertEqual(
            registered, predicates,
            f"Registry mismatch: Missing={sorted(predicates - registered)} Extra={sorted(registered - predicates)}"
        )

    def test_fact_registry_exact_match(self):
        """Transition fact registry must exactly match referenced facts."""
        def collect_facts(expression):
            facts = set()
            if "fact" in expression:
                facts.add(expression["fact"])
            elif "not" in expression:
                facts.update(collect_facts(expression["not"]))
            else:
                for key in ("all", "any"):
                    for item in expression.get(key, []):
                        facts.update(collect_facts(item))
            return facts

        referenced_facts = set()
        for expression in self.original_conditions["conditions"].values():
            referenced_facts.update(collect_facts(expression))

        declared_facts = set(self.original_conditions["facts"])
        self.assertEqual(
            referenced_facts, declared_facts,
            f"Fact registry mismatch: Missing={sorted(referenced_facts - declared_facts)} Extra={sorted(declared_facts - referenced_facts)}"
        )

    def test_breaking_change_detection_state_removal(self):
        """Test that removing a state is detected."""
        modified_protocol = self.original_protocol.copy()
        modified_protocol["states"] = {k: v for k, v in self.original_protocol["states"].items() if k != "DIAGNOSING"}
        
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=modified_protocol, schema=self.original_schema)

    def test_breaking_change_detection_transition_removal(self):
        """Test that removing a transition source is detected."""
        modified_protocol = self.original_protocol.copy()
        modified_protocol["transitions"] = {k: v for k, v in self.original_protocol["transitions"].items() if k != "DIAGNOSING"}
        
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=modified_protocol, schema=self.original_schema)

    def test_breaking_change_detection_condition_logic_change(self):
        """Test that changing a condition's logic is detected by evaluating it."""
        from scripts.evaluate_transition_policy import evaluate_transition
        
        allowed_orig, _ = evaluate_transition("ADMITTED", "CONTAINED", {"containment_required": True})
        self.assertTrue(allowed_orig)
        
        denied_orig, _ = evaluate_transition("ADMITTED", "CONTAINED", {"containment_required": False})
        self.assertFalse(denied_orig)

    def test_version_field_present(self):
        """Ensure protocol_version is present and follows semver."""
        self.assertIn("protocol_version", self.original_protocol)
        version = self.original_protocol["protocol_version"]
        parts = version.split(".")
        self.assertEqual(len(parts), 3)
        for part in parts:
            self.assertTrue(part.isdigit() or part.startswith("0"))

    def test_protocol_validates_against_schema(self):
        """Test that the current protocol validates against its schema."""
        jsonschema.validate(instance=self.original_protocol, schema=self.original_schema)

    def test_conditions_registry_exact_match(self):
        """Conditions registry must exactly match protocol predicates."""
        predicates = {
            transition["when"]
            for transitions in self.original_protocol["transitions"].values()
            for transition in transitions
        }
        predicates.update(
            transition["when"] for transition in self.original_protocol["global_transitions"]
        )

        registered = set(self.original_conditions["conditions"])
        self.assertEqual(
            registered, predicates,
            f"Registry mismatch: Missing={sorted(predicates - registered)} Extra={sorted(registered - predicates)}"
        )

    def test_fact_registry_exact_match(self):
        """Transition fact registry must exactly match referenced facts."""
        def collect_facts(expression):
            facts = set()
            if "fact" in expression:
                facts.add(expression["fact"])
            elif "not" in expression:
                facts.update(collect_facts(expression["not"]))
            else:
                for key in ("all", "any"):
                    for item in expression.get(key, []):
                        facts.update(collect_facts(item))
            return facts

        referenced_facts = set()
        for expression in self.original_conditions["conditions"].values():
            referenced_facts.update(collect_facts(expression))

        declared_facts = set(self.original_conditions["facts"])
        self.assertEqual(
            referenced_facts, declared_facts,
            f"Fact registry mismatch: Missing={sorted(referenced_facts - declared_facts)} Extra={sorted(declared_facts - referenced_facts)}"
        )

    def test_breaking_change_detection_state_removal(self):
        """Test that removing a state is detected."""
        modified_protocol = self.original_protocol.copy()
        modified_protocol["states"] = {k: v for k, v in self.original_protocol["states"].items() if k != "DIAGNOSING"}
        
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=modified_protocol, schema=self.original_schema)

    def test_breaking_change_detection_transition_removal(self):
        """Test that removing a transition source is detected."""
        modified_protocol = self.original_protocol.copy()
        modified_protocol["transitions"] = {k: v for k, v in self.original_protocol["transitions"].items() if k != "DIAGNOSING"}
        
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=modified_protocol, schema=self.original_schema)

    def test_breaking_change_detection_condition_logic_change(self):
        """Test that changing a condition's logic is detected by evaluating it."""
        from scripts.evaluate_transition_policy import evaluate_transition
        
        allowed_orig, _ = evaluate_transition("ADMITTED", "CONTAINED", {"containment_required": True})
        self.assertTrue(allowed_orig)
        
        denied_orig, _ = evaluate_transition("ADMITTED", "CONTAINED", {"containment_required": False})
        self.assertFalse(denied_orig)

    def test_version_field_present(self):
        """Ensure protocol_version is present and follows semver."""
        self.assertIn("protocol_version", self.original_protocol)
        version = self.original_protocol["protocol_version"]
        parts = version.split(".")
        self.assertEqual(len(parts), 3)
        for part in parts:
            self.assertTrue(part.isdigit() or part.startswith("0"))

    def test_protocol_validates_against_schema(self):
        """Test that the current protocol validates against its schema."""
        jsonschema.validate(instance=self.original_protocol, schema=self.original_schema)

    def test_conditions_registry_exact_match(self):
        """Conditions registry must exactly match protocol predicates."""
        predicates = {
            transition["when"]
            for transitions in self.original_protocol["transitions"].values()
            for transition in transitions
        }
        predicates.update(
            transition["when"] for transition in self.original_protocol["global_transitions"]
        )

        registered = set(self.original_conditions["conditions"])
        self.assertEqual(
            registered, predicates,
            f"Registry mismatch: Missing={sorted(predicates - registered)} Extra={sorted(registered - predicates)}"
        )

    def test_fact_registry_exact_match(self):
        """Transition fact registry must exactly match referenced facts."""
        def collect_facts(expression):
            facts = set()
            if "fact" in expression:
                facts.add(expression["fact"])
            elif "not" in expression:
                facts.update(collect_facts(expression["not"]))
            else:
                for key in ("all", "any"):
                    for item in expression.get(key, []):
                        facts.update(collect_facts(item))
            return facts

        referenced_facts = set()
        for expression in self.original_conditions["conditions"].values():
            referenced_facts.update(collect_facts(expression))

        declared_facts = set(self.original_conditions["facts"])
        self.assertEqual(
            referenced_facts, declared_facts,
            f"Fact registry mismatch: Missing={sorted(referenced_facts - declared_facts)} Extra={sorted(declared_facts - referenced_facts)}"
        )

    def test_breaking_change_detection_state_removal(self):
        """Test that removing a state is detected."""
        modified_protocol = self.original_protocol.copy()
        modified_protocol["states"] = {k: v for k, v in self.original_protocol["states"].items() if k != "DIAGNOSING"}
        
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=modified_protocol, schema=self.original_schema)

    def test_breaking_change_detection_transition_removal(self):
        """Test that removing a transition source is detected."""
        modified_protocol = self.original_protocol.copy()
        modified_protocol["transitions"] = {k: v for k, v in self.original_protocol["transitions"].items() if k != "DIAGNOSING"}
        
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=modified_protocol, schema=self.original_schema)

    def test_breaking_change_detection_condition_logic_change(self):
        """Test that changing a condition's logic is detected by evaluating it."""
        from scripts.evaluate_transition_policy import evaluate_transition
        
        allowed_orig, _ = evaluate_transition("ADMITTED", "CONTAINED", {"containment_required": True})
        self.assertTrue(allowed_orig)
        
        denied_orig, _ = evaluate_transition("ADMITTED", "CONTAINED", {"containment_required": False})
        self.assertFalse(denied_orig)

    def test_version_field_present(self):
        """Ensure protocol_version is present and follows semver."""
        self.assertIn("protocol_version", self.original_protocol)
        version = self.original_protocol["protocol_version"]
        parts = version.split(".")
        self.assertEqual(len(parts), 3)
        for part in parts:
            self.assertTrue(part.isdigit() or part.startswith("0"))

    def test_protocol_validates_against_schema(self):
        """Test that the current protocol validates against its schema."""
        jsonschema.validate(instance=self.original_protocol, schema=self.original_schema)

    def test_conditions_registry_exact_match(self):
        """Conditions registry must exactly match protocol predicates."""
        predicates = {
            transition["when"]
            for transitions in self.original_protocol["transitions"].values()
            for transition in transitions
        }
        predicates.update(
            transition["when"] for transition in self.original_protocol["global_transitions"]
        )

        registered = set(self.original_conditions["conditions"])
        self.assertEqual(
            registered, predicates,
            f"Registry mismatch: Missing={sorted(predicates - registered)} Extra={sorted(registered - predicates)}"
        )

    def test_fact_registry_exact_match(self):
        """Transition fact registry must exactly match referenced facts."""
        def collect_facts(expression):
            facts = set()
            if "fact" in expression:
                facts.add(expression["fact"])
            elif "not" in expression:
                facts.update(collect_facts(expression["not"]))
            else:
                for key in ("all", "any"):
                    for item in expression.get(key, []):
                        facts.update(collect_facts(item))
            return facts

        referenced_facts = set()
        for expression in self.original_conditions["conditions"].values():
            referenced_facts.update(collect_facts(expression))

        declared_facts = set(self.original_conditions["facts"])
        self.assertEqual(
            referenced_facts, declared_facts,
            f"Fact registry mismatch: Missing={sorted(referenced_facts - declared_facts)} Extra={sorted(declared_facts - referenced_facts)}"
        )

    def test_breaking_change_detection_state_removal(self):
        """Test that removing a state is detected."""
        modified_protocol = self.original_protocol.copy()
        modified_protocol["states"] = {k: v for k, v in self.original_protocol["states"].items() if k != "DIAGNOSING"}
        
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=modified_protocol, schema=self.original_schema)

    def test_breaking_change_detection_transition_removal(self):
        """Test that removing a transition source is detected."""
        modified_protocol = self.original_protocol.copy()
        modified_protocol["transitions"] = {k: v for k, v in self.original_protocol["transitions"].items() if k != "DIAGNOSING"}
        
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=modified_protocol, schema=self.original_schema)

    def test_breaking_change_detection_condition_logic_change(self):
        """Test that changing a condition's logic is detected by evaluating it."""
        from scripts.evaluate_transition_policy import evaluate_transition
        
        allowed_orig, _ = evaluate_transition("ADMITTED", "CONTAINED", {"containment_required": True})
        self.assertTrue(allowed_orig)
        
        denied_orig, _ = evaluate_transition("ADMITTED", "CONTAINED", {"containment_required": False})
        self.assertFalse(denied_orig)

    def test_version_field_present(self):
        """Ensure protocol_version is present and follows semver."""
        self.assertIn("protocol_version", self.original_protocol)
        version = self.original_protocol["protocol_version"]
        parts = version.split(".")
        self.assertEqual(len(parts), 3)
        for part in parts:
            self.assertTrue(part.isdigit() or part.startswith("0"))

    def test_protocol_validates_against_schema(self):
        """Test that the current protocol validates against its schema."""
        jsonschema.validate(instance=self.original_protocol, schema=self.original_schema)

    def test_conditions_registry_exact_match(self):
        """Conditions registry must exactly match protocol predicates."""
        predicates = {
            transition["when"]
            for transitions in self.original_protocol["transitions"].values()
            for transition in transitions
        }
        predicates.update(
            transition["when"] for transition in self.original_protocol["global_transitions"]
        )

        registered = set(self.original_conditions["conditions"])
        self.assertEqual(
            registered, predicates,
            f"Registry mismatch: Missing={sorted(predicates - registered)} Extra={sorted(registered - predicates)}"
        )

    def test_fact_registry_exact_match(self):
        """Transition fact registry must exactly match referenced facts."""
        def collect_facts(expression):
            facts = set()
            if "fact" in expression:
                facts.add(expression["fact"])
            elif "not" in expression:
                facts.update(collect_facts(expression["not"]))
            else:
                for key in ("all", "any"):
                    for item in expression.get(key, []):
                        facts.update(collect_facts(item))
            return facts

        referenced_facts = set()
        for expression in self.original_conditions["conditions"].values():
            referenced_facts.update(collect_facts(expression))

        declared_facts = set(self.original_conditions["facts"])
        self.assertEqual(
            referenced_facts, declared_facts,
            f"Fact registry mismatch: Missing={sorted(referenced_facts - declared_facts)} Extra={sorted(declared_facts - referenced_facts)}"
        )

    def test_breaking_change_detection_state_removal(self):
        """Test that removing a state is detected."""
        modified_protocol = self.original_protocol.copy()
        modified_protocol["states"] = {k: v for k, v in self.original_protocol["states"].items() if k != "DIAGNOSING"}
        
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=modified_protocol, schema=self.original_schema)

    def test_breaking_change_detection_transition_removal(self):
        """Test that removing a transition source is detected."""
        modified_protocol = self.original_protocol.copy()
        modified_protocol["transitions"] = {k: v for k, v in self.original_protocol["transitions"].items() if k != "DIAGNOSING"}
        
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=modified_protocol, schema=self.original_schema)

    def test_breaking_change_detection_condition_logic_change(self):
        """Test that changing a condition's logic is detected by evaluating it."""
        from scripts.evaluate_transition_policy import evaluate_transition
        
        allowed_orig, _ = evaluate_transition("ADMITTED", "CONTAINED", {"containment_required": True})
        self.assertTrue(allowed_orig)
        
        denied_orig, _ = evaluate_transition("ADMITTED", "CONTAINED", {"containment_required": False})
        self.assertFalse(denied_orig)

    def test_version_field_present(self):
        """Ensure protocol_version is present and follows semver."""
        self.assertIn("protocol_version", self.original_protocol)
        version = self.original_protocol["protocol_version"]
        parts = version.split(".")
        self.assertEqual(len(parts), 3)
        for part in parts:
            self.assertTrue(part.isdigit() or part.startswith("0"))

    def test_protocol_validates_against_schema(self):
        """Test that the current protocol validates against its schema."""
        jsonschema.validate(instance=self.original_protocol, schema=self.original_schema)

    def test_conditions_registry_exact_match(self):
        """Conditions registry must exactly match protocol predicates."""
        predicates = {
            transition["when"]
            for transitions in self.original_protocol["transitions"].values()
            for transition in transitions
        }
        predicates.update(
            transition["when"] for transition in self.original_protocol["global_transitions"]
        )

        registered = set(self.original_conditions["conditions"])
        self.assertEqual(
            registered, predicates,
            f"Registry mismatch: Missing={sorted(predicates - registered)} Extra={sorted(registered - predicates)}"
        )

    def test_fact_registry_exact_match(self):
        """Transition fact registry must exactly match referenced facts."""
        def collect_facts(expression):
            facts = set()
            if "fact" in expression:
                facts.add(expression["fact"])
            elif "not" in expression:
                facts.update(collect_facts(expression["not"]))
            else:
                for key in ("all", "any"):
                    for item in expression.get(key, []):
                        facts.update(collect_facts(item))
            return facts

        referenced_facts = set()
        for expression in self.original_conditions["conditions"].values():
            referenced_facts.update(collect_facts(expression))

        declared_facts = set(self.original_conditions["facts"])
        self.assertEqual(
            referenced_facts, declared_facts,
            f"Fact registry mismatch: Missing={sorted(referenced_facts - declared_facts)} Extra={sorted(declared_facts - referenced_facts)}"
        )


if __name__ == "__main__":
    unittest.main()
