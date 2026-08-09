# External Transcription Service Registry

**Purpose:** operational fallback/convenience list for transcription services that can accept audio/video files.  
**Status model:** `DISCOVERED → SOURCE_VERIFIED → PRIVACY_REVIEWED → TESTED → APPROVED`.  
**Default status of every entry below:** **DISCOVERED / USE WITH CAUTION** unless explicitly promoted later.

> Registry presence is not a security approval and is not a recommendation to upload sensitive material.

## Mandatory caution

Do not upload confidential, regulated, evidentiary or otherwise sensitive files merely because a service is convenient. Before use, check the provider's current terms, privacy/data-retention controls, deletion behavior, processing jurisdiction, account security, and whether your organization/contract permits third-party processing.

For FATHER, the strategic target remains local-first transcription. These services are fallback, comparison and emergency options.

## Discovered services — verified as available on 2026-08-09

| Service | Website | Observed capability | Registry status | Caution |
|---|---|---|---|---|
| AssemblyAI Playground / API | https://www.assemblyai.com/ | Web Playground can accept uploaded audio; API supports common audio/video formats and file upload/public URL workflows | DISCOVERED / SOURCE-VERIFIED | AssemblyAI itself warns its public Playground has limited functionality and sensitive data should not be uploaded there; use API/data-security review separately |
| Deepgram | https://deepgram.com/ | Speech-to-text platform; web examples support using/uploading your own file and developer API/CLI supports file/URL transcription | DISCOVERED | Cloud processing; review retention, region, account and contractual controls before non-public data |
| TurboScribe | https://turboscribe.ai/ | Browser upload of common audio/video formats; transcription, speaker recognition and exports | DISCOVERED | Consumer web upload path; provider privacy/security claims must be independently reviewed before sensitive files |
| ElevenLabs Scribe | https://elevenlabs.io/audio-to-text | Browser upload of common audio/video; multilingual transcription, timestamps/speaker labels and exports | DISCOVERED | Cloud upload; perform privacy/legal review before non-public recordings |
| Otter.ai | https://otter.ai/ | Imports audio/video files for automatic transcription and meeting-note features | DISCOVERED | Cloud collaboration product; uploaded conversations may become part of account/workspace history; review sharing, retention and plan controls |

## Planned evaluation fields

When this registry becomes operational, each service card should include:

```text
provider_id
verified_at
website
service_type: web_ui | api | both
supported_input_types
max_file_size
max_duration
languages
speaker_diarization
timestamps
export_formats
price_snapshot
retention_policy_reference
delete_control
training_use_policy
processing_regions
security/compliance claims
api_available
failure/fallback behavior
FATHER_status
WHY
```

## Use policy candidate

```text
PUBLIC artifact
   ↓
external service MAY be considered

INTERNAL artifact
   ↓
explicit operator/policy approval required

CONFIDENTIAL / RESTRICTED / EVIDENCE
   ↓
LOCAL-FIRST by default
   ↓
external processing only after a separately approved exception
```

The exact classes are not yet approved domain policy; this is the design direction.

## Maintenance

This list is time-sensitive. Services, pricing, limits, data terms and availability change. Before operational use, re-verify the service and stamp `verified_at`. Do not let a year-old card silently remain APPROVED.
