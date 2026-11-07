//! Get any `preprocessor.trpl-*` config.

use mdbook_preprocessor::PreprocessorContext;

#[derive(Debug, Default, Clone, Copy, PartialEq, serde::Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Mode {
    #[default]
    Default,
    Simple,
}

impl Mode {
    pub fn from_context(
        ctx: &PreprocessorContext,
        preprocessor_name: &str,
    ) -> Result<Mode, Error> {
        #[derive(Default, serde::Deserialize)]
        #[serde(rename_all = "kebab-case")]
        struct Config {
            #[serde(default)]
            output_mode: Mode,
        }

        let config: Config = ctx
            .config
            .get(&format!("preprocessor.{preprocessor_name}"))?
            .ok_or_else(|| Error::NoConfig(preprocessor_name.into()))?;
        Ok(config.output_mode)
    }
}

/// User-visible labels emitted by the preprocessors, configurable so that
/// translations of the book can localize them. The defaults are English.
///
/// ```toml
/// [preprocessor.trpl-listing]
/// listing-label = "{number}. kódrészlet"
/// file-name-label = "Fájlnév"
///
/// [preprocessor.trpl-note]
/// note-prefix = "Megjegyzés: "
/// ```
#[derive(Debug, Clone, PartialEq, serde::Deserialize)]
#[serde(rename_all = "kebab-case", default)]
pub struct Labels {
    /// Template for a listing label; `{number}` is replaced by the number.
    pub listing_label: String,
    /// Label shown before a listing's file name.
    pub file_name_label: String,
    /// Prefix which marks a blockquote as a semantic note.
    pub note_prefix: String,
}

impl Default for Labels {
    fn default() -> Self {
        Labels {
            listing_label: String::from("Listing {number}"),
            file_name_label: String::from("Filename"),
            note_prefix: String::from("Note: "),
        }
    }
}

impl Labels {
    pub fn from_context(
        ctx: &PreprocessorContext,
        preprocessor_name: &str,
    ) -> Result<Labels, Error> {
        Ok(ctx
            .config
            .get(&format!("preprocessor.{preprocessor_name}"))?
            .unwrap_or_default())
    }

    pub fn listing(&self, number: &str) -> String {
        self.listing_label.replace("{number}", number)
    }
}

#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error(transparent)]
    Mdbook(#[from] mdbook_preprocessor::errors::Error),

    #[error("No config for '{0}'")]
    NoConfig(String),
}

#[cfg(test)]
mod tests;
